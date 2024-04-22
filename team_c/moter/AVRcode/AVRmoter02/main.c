#define F_CPU 16000000L
#include <avr/io.h>
#include <util/delay.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "UART.h"

#define ROTATION_DELAY 	10000
#define PULSE_00		1200
#define PULSE_45		2100
#define PULSE_90		3150
#define PULSE_135		4000
#define PULSE_180		5000

void INIT_TIMER1(void)
{
	// Fast PWM 모드, TOP = ICR1
	TCCR1A |= (1 << WGM11);
	TCCR1B |= (1 << WGM12) | (1 << WGM13);
	TCCR1B |= (1 << CS11);		// 분주율 8, 2MHz
	TCCR1A |= (1 << COM1A1);		// 비반전 모드
	ICR1 = 40000;				// 20ms 주기
	DDRB = 0xFF;
	PORTB = 0x00;
}

int main(void)
{
	int index = 0;			// 수신 버퍼에 저장할 위치
	char buffer[20] = "";		// 수신 데이터 버퍼
	char data;				// 수신 데이터
	
	UART_INIT();			// UART 통신 초기화
	INIT_TIMER1();
	
	while(1)
	{
		buffer[index] = '\0';
		index = 0;
		while(1)
		{
			buffer[index] = '\0';
			index = 0;
			data = UART_receive();
			buffer[index] = data;
			
			if(strcmp(buffer, "g") == 0){
				OCR1A = PULSE_90;
				UART_transmit(data);
				_delay_ms(ROTATION_DELAY);
				buffer[index] = '\0';
				index = 0;
				data = UART_receive();
				buffer[index] = data;
				if(strcmp(buffer, "s") == 0){
					UART_transmit(data);
					buffer[index] = '\0';
					index = 0;
					break;
				}
				else{
					OCR1A = PULSE_45;
					UART_transmit(data);
					_delay_ms(ROTATION_DELAY);
					buffer[index] = '\0';
					index = 0;
				}
				data = UART_receive();
				buffer[index] = data;
				if(strcmp(buffer, "s") == 0){
					UART_transmit(data);
					buffer[index] = '\0';
					index = 0;
					break;
				}
				else{
					OCR1A = PULSE_00;
					UART_transmit(data);
					_delay_ms(ROTATION_DELAY);
					buffer[index] = '\0';
					index = 0;
				}
				data = UART_receive();
				buffer[index] = data;
				if(strcmp(buffer, "s") == 0){
					UART_transmit(data);
					buffer[index] = '\0';
					index = 0;
					break;
				}
				else{
					OCR1A = PULSE_45;
					UART_transmit(data);
					_delay_ms(ROTATION_DELAY);
					buffer[index] = '\0';
					index = 0;
				}
				
				data = UART_receive();
				buffer[index] = data;
				if(strcmp(buffer, "s") == 0){
					UART_transmit(data);
					buffer[index] = '\0';
					index = 0;
					break;
				}
				else{
					OCR1A = PULSE_90;
					UART_transmit(data);
					_delay_ms(ROTATION_DELAY);
					buffer[index] = '\0';
					index = 0;
				}
				data = UART_receive();
				buffer[index] = data;
				if(strcmp(buffer, "s") == 0){
					UART_transmit(data);
					buffer[index] = '\0';
					index = 0;
					break;
				}
				else{
					OCR1A = PULSE_135;
					UART_transmit(data);
					_delay_ms(ROTATION_DELAY);
					buffer[index] = '\0';
					index = 0;
				}
				data = UART_receive();
				buffer[index] = data;
				if(strcmp(buffer, "s") == 0){
					UART_transmit(data);
					buffer[index] = '\0';
					index = 0;
					break;
				}
				else{
					OCR1A = PULSE_180;
					UART_transmit(data);
					_delay_ms(ROTATION_DELAY);
					buffer[index] = '\0';
					index = 0;
				}
				data = UART_receive();
				buffer[index] = data;
				if(strcmp(buffer, "s") == 0){
					UART_transmit(data);
					buffer[index] = '\0';
					index = 0;
					break;
				}
				else{
					OCR1A = PULSE_135;
					UART_transmit(data);
					_delay_ms(ROTATION_DELAY);
					buffer[index] = '\0';
					index = 0;
				}
				data = UART_receive();
				buffer[index] = data;
				if(strcmp(buffer, "s") == 0){
					UART_transmit(data);
					buffer[index] = '\0';
					index = 0;
					break;
				}
				else{
					UART_transmit(data);
					buffer[index] = '\0';
					index = 0;
				}
			}
			else if(strcmp(buffer, "s") == 0){
				UART_transmit(data);
				PORTB = (0x04) | (0x08);
				_delay_ms(200);
				PORTB = 0x00;
				buffer[index] = '\0';
				index = 0;
			}
			else{
				UART_transmit(data);
				buffer[index] = '\0';
				index = 0;
			}
		}
	}
}