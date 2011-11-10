#ifndef _LIBMPSSE_H_ 
#define _LIBMPSSE_H_

#include <ftdi.h>
#include <stdint.h>

#define MPSSE_OK		0
#define MPSSE_FAIL		1

#define MSB			0x00
#define LSB			0x08

#define TRANSFER_SIZE		((64 * 1024) - 1)

#define LATENCY_MS		2
#define MAX_TIMEOUT_MS		5000
#define TIMEOUT_MS		10000
#define TIMEOUT_DIVISOR		1000000

#define BITMODE_RESET		0
#define BITMODE_MPSSE		2

#define CMD_SIZE		3
#define SS_TX_COUNT		3

/* Common clock rates */
enum clock_rates
{
	ONE_HUNDRED_KHZ  = 100000,
	TWO_HUNDRED_KHZ  = 200000,
	FOUR_HUNDRED_KHZ = 400000,
	ONE_MHZ 	 = 1000000,
	SIX_MHZ 	 = 6000000,
	TWELVE_MHZ 	 = 12000000,
	THIRTY_MHZ 	 = 30000000,
	SIXTY_MHZ 	 = 60000000
};

/* Supported MPSSE modes */
enum modes
{
	SPI0 = 1,
	SPI1 = 2,
	SPI2 = 3,
	SPI3 = 4,
	I2C  = 5
};

enum pins
{
	SK	= 1,
	DO	= 2,
	DI	= 4,
	CS	= 8 ,
	GPIO0	= 16,
	GPIO1	= 32,
	GPIO2	= 64,
	GPIO3	= 128
};

#define DEFAULT_TRIS            (SK | DO | CS)  /* SK/DO/CS are outputs, all others inputs */
#define DEFAULT_PORT            (SK | CS)       /* SK and CS are high, all others low */

enum mpsse_commands
{
	INVALID_COMMAND		= 0xAB,
	ENABLE_3_PHASE_CLOCK	= 0x8C,
	DISABLE_3_PHASE_CLOCK	= 0x8D,
	DISABLE_ADAPTIVE_CLOCK	= 0x97,
	TCK_X5			= 0x8A,
	TCK_D5			= 0x8B,
	TOGGLE_CLOCK		= 0x8E
};

struct vid_pid
{
	int vid;
	int pid;
	char *description;
};

struct globule
{
	char *description;
	enum modes mode;
	struct ftdi_context ftdi;
	int vid;
	int pid;
	int clock;
	char tris;
	char pstart;
	char pstop;
	char pidle;
	uint8_t tx;
	uint8_t rx;
	uint8_t tack;
	uint8_t rack;
} mpsse;

int MPSSE(enum modes mode, int freq, int endianess);
int Open(int vid, int pid, enum modes mode, int freq, int endianess);
void Close(void);
char *ErrorString(void);
void SetTimeouts(int timeout);
int SetMode(enum modes mode, int endianess);
int SetClock(uint32_t freq);
int GetClock(void);
int GetVid(void);
int GetPid(void);
char *GetDescription(void);
int SetLoopback(int enable);
int Start(void);
int Write(char *data, int size);
int Stop(void);
int GetAck(void);
void SetAck(int ack);

#ifdef SWIGPYTHON

typedef struct swig_string_data
{
        int size;
        char *data;
} swig_string_data;

swig_string_data Read(int size);

#else

char *Read(int size);

#endif

#endif