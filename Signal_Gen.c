//*****************************************************************************
// Copyright (c) 2012-2020 Texas Instruments Incorporated.  All rights reserved.
// Software License Agreement
// 
// Texas Instruments (TI) is supplying this software for use solely and
// exclusively on TI's microcontroller products. The software is owned by
// TI and/or its suppliers, and is protected under applicable copyright
// laws. You may not combine this software with "viral" open-source
// software in order to form a larger program.
// 
// THIS SOFTWARE IS PROVIDED "AS IS" AND WITH ALL FAULTS.
// NO WARRANTIES, WHETHER EXPRESS, IMPLIED OR STATUTORY, INCLUDING, BUT
// NOT LIMITED TO, IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
// A PARTICULAR PURPOSE APPLY TO THIS SOFTWARE. TI SHALL NOT, UNDER ANY
// CIRCUMSTANCES, BE LIABLE FOR SPECIAL, INCIDENTAL, OR CONSEQUENTIAL
// DAMAGES, FOR ANY REASON WHATSOEVER.
// 
// This is part of revision 2.2.0.295 of the EK-TM4C123GXL Firmware Package.
//
//*****************************************************************************
//*****************************************************************************
//
// hello.c - Simple hello world example.
//
// Copyright (c) 2012-2020 Texas Instruments Incorporated.  All rights reserved.
// Software License Agreement
// 
// Texas Instruments (TI) is supplying this software for use solely and
// exclusively on TI's microcontroller products. The software is owned by
// TI and/or its suppliers, and is protected under applicable copyright
// laws. You may not combine this software with "viral" open-source
// software in order to form a larger program.
// 
// THIS SOFTWARE IS PROVIDED "AS IS" AND WITH ALL FAULTS.
// NO WARRANTIES, WHETHER EXPRESS, IMPLIED OR STATUTORY, INCLUDING, BUT
// NOT LIMITED TO, IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
// A PARTICULAR PURPOSE APPLY TO THIS SOFTWARE. TI SHALL NOT, UNDER ANY
// CIRCUMSTANCES, BE LIABLE FOR SPECIAL, INCIDENTAL, OR CONSEQUENTIAL
// DAMAGES, FOR ANY REASON WHATSOEVER.
// 
// This is part of revision 2.2.0.295 of the EK-TM4C123GXL Firmware Package.
//
//*****************************************************************************

#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "inc/hw_memmap.h"
#include "inc/hw_gpio.h"
#include "inc/hw_types.h"

#include "driverlib/gpio.h"
#include "driverlib/sysctl.h"
#include "driverlib/uart.h"
#include "driverlib/pin_map.h"
#include "driverlib/rom_map.h"

#include "utils/uartstdio.h"

//====================================================
// GLOBAL STATE & BUFFERING
//====================================================
bool bp_mode = false;      // False = Simulation, True = Real Sensor
bool last_button = true;   // For debouncing PF4
bool bp_valid = false;     // Tracks if a 'success' packet was received

uint32_t last_sys = 0, last_dia = 0, last_pulse = 0;

static char rx_buffer[64];
static int rx_idx = 0;

//====================================================
// PERIPHERAL CONFIGURATION
//====================================================
void ConfigureUART(void) {
    // UART0 -> PC (USB Debug) @ 115200
    MAP_SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);
    MAP_SysCtlPeripheralEnable(SYSCTL_PERIPH_UART0);
    MAP_GPIOPinConfigure(GPIO_PA0_U0RX);
    MAP_GPIOPinConfigure(GPIO_PA1_U0TX);
    MAP_GPIOPinTypeUART(GPIO_PORTA_BASE, GPIO_PIN_0 | GPIO_PIN_1);
    UARTStdioConfig(0, 115200, MAP_SysCtlClockGet());

    // UART1 -> BP Sensor (PB0/PB1) @ 9600
    MAP_SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOB);
    MAP_SysCtlPeripheralEnable(SYSCTL_PERIPH_UART1);
    MAP_GPIOPinConfigure(GPIO_PB0_U1RX);
    MAP_GPIOPinConfigure(GPIO_PB1_U1TX);
    MAP_GPIOPinTypeUART(GPIO_PORTB_BASE, GPIO_PIN_0 | GPIO_PIN_1);

    MAP_UARTConfigSetExpClk(UART1_BASE, MAP_SysCtlClockGet(), 9600,
                            (UART_CONFIG_WLEN_8 | UART_CONFIG_STOP_ONE | UART_CONFIG_PAR_NONE));
}

void ConfigureButton(void) {
    // Enable Port F for Button (PF4) and RGB LEDs
    MAP_SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);
    
    // Unlock PF0 (if needed) and configure PF4 as Input with Pull-up
    HWREG(GPIO_PORTF_BASE + GPIO_O_LOCK) = GPIO_LOCK_KEY;
    HWREG(GPIO_PORTF_BASE + GPIO_O_CR) |= GPIO_PIN_4;
    MAP_GPIOPinTypeGPIOInput(GPIO_PORTF_BASE, GPIO_PIN_4);
    MAP_GPIOPadConfigSet(GPIO_PORTF_BASE, GPIO_PIN_4, GPIO_STRENGTH_2MA, GPIO_PIN_TYPE_STD_WPU);

    // RGB LEDs: Red (PF1), Blue (PF2), Green (PF3)
    MAP_GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE, GPIO_PIN_1 | GPIO_PIN_2 | GPIO_PIN_3);
}

//====================================================
// BP SENSOR PARSER
//====================================================
bool ReadBP_NonBlocking(uint32_t *sys, uint32_t *dia, uint32_t *pulse) {
    while (UARTCharsAvail(UART1_BASE)) {
        char c = UARTCharGet(UART1_BASE);
        if (c == '\n' || c == '\r') {
            if (rx_idx == 0) continue;
            rx_buffer[rx_idx] = '\0';
            rx_idx = 0;

            uint32_t s, d, p;
            // Matches: "success,SYS,DIA,PULSE"
            if (sscanf(rx_buffer, "success,%u,%u,%u", &s, &d, &p) == 3) {
                *sys = s;
                *dia = d;
                *pulse = p;
                return true;
            }
        } else if (rx_idx < 63) {
            rx_buffer[rx_idx++] = c;
        }
    }
    return false;
}

//====================================================
// MAIN APPLICATION LOOP
//====================================================
int main(void) {
    // Set system clock to 40MHz
    MAP_SysCtlClockSet(SYSCTL_SYSDIV_5 | SYSCTL_USE_PLL | SYSCTL_XTAL_16MHZ | SYSCTL_OSC_MAIN);

    ConfigureUART();
    ConfigureButton();

    uint32_t print_timer = 0;
    uint32_t cur_sys, cur_dia, cur_pulse;
    int hr, spo2, rr, tempInt, tempDec, sim_sys, sim_dia, anomaly_trigger;

    // Initialization Prompt
    UARTprintf("--- Physiological Data Logger Initialized ---\n");

    while (1) {
        // 1. Always listen for BP Sensor packets
        if (ReadBP_NonBlocking(&cur_sys, &cur_dia, &cur_pulse)) {
            last_sys = cur_sys;
            last_dia = cur_dia;
            last_pulse = cur_pulse;
            bp_valid = true;
        }

        // 2. Monitor Mode Toggle Button (PF4)
        bool current_btn = (GPIOPinRead(GPIO_PORTF_BASE, GPIO_PIN_4) == 0);
        if (current_btn && !last_button) {
            SysCtlDelay(MAP_SysCtlClockGet() / 150); // Small debounce
            bp_mode = !bp_mode;
            bp_valid = false; // Reset validity so user sees 'Waiting' state on switch
        }
        last_button = current_btn;

        // 3. Data Output Transmission (Approx every 3 seconds)
        if (++print_timer >= 300) {
            print_timer = 0;

            if (bp_mode) {
                // --- REAL SENSOR MODE ---
                if (bp_valid) {
                    // BLUE LED: Data Acquired
                    GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_1|GPIO_PIN_2|GPIO_PIN_3, GPIO_PIN_2);
                    UARTprintf("%u,NaN,NaN,NaN,%u,%u\n", last_pulse, last_sys, last_dia);
                } else {
                    // RED LED: Waiting for Measurement
                    GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_1|GPIO_PIN_2|GPIO_PIN_3, GPIO_PIN_1);
                    UARTprintf("NaN,NaN,NaN,NaN,NaN,NaN\n");
                }
            } 
            else {
                // --- SIMULATION MODE (GREEN LED) ---
                GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_1|GPIO_PIN_2|GPIO_PIN_3, GPIO_PIN_3);
                
                anomaly_trigger = rand() % 5; 

                if (anomaly_trigger == 0) {
                    // CRITICAL/ABNORMAL VALUES (20% probability)
                    hr = 145 + (rand() % 30);
                    spo2 = 84 + (rand() % 6);
                    rr = 28 + (rand() % 8);
                    tempInt = 39 + (rand() % 2);
                    tempDec = rand() % 9;
                    sim_sys = 160 + (rand() % 25);
                    sim_dia = 100 + (rand() % 15);
                } else {
                    // NORMAL VALUES (80% probability)
                    hr = 68 + (rand() % 20);
                    spo2 = 96 + (rand() % 4);
                    rr = 12 + (rand() % 6);
                    tempInt = 36;
                    tempDec = 2 + (rand() % 7);
                    sim_sys = 110 + (rand() % 15);
                    sim_dia = 70 + (rand() % 15);
                }
                
                // Format for Python: HR, SpO2, RR, Temp, SYS, DIA
                UARTprintf("%d,%d,%d,%d.%d,%d,%d\n", hr, spo2, rr, tempInt, tempDec, sim_sys, sim_dia);
            }
        }

        // Loop runs every 10ms (approx)
        SysCtlDelay(MAP_SysCtlClockGet() / 300);
    }
}
