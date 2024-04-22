#define F_CPU 16000000L
#include <avr/io.h>
#include <util/delay.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "UART.h"

#define ROTATION_DELAY 	1500
#define PULSE_00		1200
#define PULSE_45		2100
#define PULSE_90		3150
#define PULSE_135		4000
#define PULSE_180		5000

void INIT_TIMER1(void)
{
	// Fast PWM ���, TOP = ICR1
	TCCR1A |= (1 << WGM11);
	TCCR1B |= (1 << WGM12) | (1 << WGM13);
	TCCR1B |= (1 << CS11);		// ������ 8, 2MHz
	TCCR1A |= (1 << COM1A1);		// ����� ���
	ICR1 = 40000;				// 20ms �ֱ�
	DDRB = 0xFF;
	PORTB = 0x00;
}

int main(void)
{
	int index = 0;			// ���� ���ۿ� ������ ��ġ
	char buffer[20] = "";		// ���� ������ ����
	char data;				// ���� ������
	
	UART_INIT();			// UART ��� �ʱ�ȭ
	INIT_TIMER1();
	
	while(1)
	{
		data = UART_receive();	// ������ ����
		buffer[index] = data;
		
		if(strcmp(buffer, "q") == 0){	
			OCR1A = PULSE_00;
			UART_transmit(data);
			index = 0;
		}
		else if(strcmp(buffer, "w") == 0){
			OCR1A = PULSE_45;
			UART_transmit(data);
			index = 0;
		}
		else if(strcmp(buffer, "e") == 0){
			OCR1A = PULSE_90;
			UART_transmit(data);
			index = 0;
		}
		else if(strcmp(buffer, "r") == 0){
			OCR1A = PULSE_135;
			UART_transmit(data);
			index = 0;
		}
		else if(strcmp(buffer, "t") == 0){
			OCR1A = PULSE_180;
			UART_transmit(data);
			index = 0;
		}
		else if(strcmp(buffer, "s") == 0){
			UART_transmit(data);
			PORTB = (0x04) | (0x08);
			_delay_ms(200);
			PORTB = 0x00;
			index = 0;
		}
		else{
			UART_transmit(data);
			index = 0;
		}
	}
}