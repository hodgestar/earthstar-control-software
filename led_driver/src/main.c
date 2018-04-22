#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

#include <bcm2835.h>
#include <czmq.h>

#include "clk.h"
#include "dma.h"
#include "gpio.h"
#include "pwm.h"
#include "ws2811.h"

#define RED           0x00200000
#define ORANGE        0x00201000
#define YELLOW        0x00202000
#define GREEN         0x00002000
#define LIGHT_BLUE    0x00002020
#define BLUE          0x00000020
#define PURPLE        0x00100010
#define PINK          0x00200010
#define WHITE         0x00202020
#define BLANK         0x00000000

#define TARGET_FREQ             WS2811_TARGET_FREQ
#define STRIP_TYPE              WS2811_STRIP_GRB		// WS2812/SK6812RGB integrated chip+leds

#define LED_COUNT_PER_RING      450
#define RINGS					6
#define BYTES_PER_LED			4

#define BYTES_PER_FRAME			(LED_COUNT_PER_RING * RINGS * BYTES_PER_LED)
#define BYTES_PER_FRAME_RING	(LED_COUNT_PER_RING * BYTES_PER_LED)

#define FRAME_0					(0 * BYTES_PER_FRAME_RING)
#define FRAME_1					(1 * BYTES_PER_FRAME_RING)
#define FRAME_2					(2 * BYTES_PER_FRAME_RING)
#define FRAME_3					(3 * BYTES_PER_FRAME_RING)
#define FRAME_4					(4 * BYTES_PER_FRAME_RING)
#define FRAME_5					(5 * BYTES_PER_FRAME_RING)

#define PWM_0_GPIO_PIN			12
#define PWM_0_CHANNEL_0_PIN		22
#define PWM_0_CHANNEL_1_PIN		27
#define PWM_1_GPIO_PIN			13
#define PWM_1_CHANNEL_0_PIN		5
#define PWM_1_CHANNEL_1_PIN		6
#define PCM_0_GPIO_PIN			21
#define PCM_0_CHANNEL_0_PIN		16
#define PCM_0_CHANNEL_1_PIN		20
#define SPI_0_GPIO_PIN			10
#define SPI_0_CHANNEL_0_PIN		NULL
#define SPI_0_CHANNEL_1_PIN		NULL

static uint8_t running = 1;
struct timespec tstart={0,0}, tend={0,0};

ws2811_t ledstring_PWM = {
    .freq = TARGET_FREQ,
    .dmanum = 10,
    .channel = {[0] = {.gpionum = PWM_0_GPIO_PIN, .count = LED_COUNT_PER_RING,
		.invert = 0, .brightness = 255, .strip_type = STRIP_TYPE,},
				[1] = {.gpionum = PWM_1_GPIO_PIN, .count = LED_COUNT_PER_RING,
        .invert = 0, .brightness = 255, .strip_type = STRIP_TYPE,},
    },};
ws2811_t ledstring_SPI = {
	.freq = TARGET_FREQ,
	.dmanum = 13,
	.channel = {[0] = {.gpionum = SPI_0_GPIO_PIN, .count = LED_COUNT_PER_RING, 
		.invert = 0, .brightness = 255, .strip_type = STRIP_TYPE, },
				[1] = {.gpionum = 0, .count = 0,
		.invert = 0, .brightness = 0, .strip_type = STRIP_TYPE, },
	},};
ws2811_t ledstring_PCM = {
	.freq = TARGET_FREQ,
	.dmanum = 14,
	.channel = {[0] = {.gpionum = PCM_0_GPIO_PIN, .count = LED_COUNT_PER_RING, 
		.invert = 0, .brightness = 255, .strip_type = STRIP_TYPE, },
				[1] = {.gpionum = 0, .count = 0,
		.invert = 0, .brightness = 0, .strip_type = STRIP_TYPE, },
	},};

void matrix_render(unsigned char * frame_0, unsigned char * frame_1,
				   unsigned char * frame_2)
{
	memcpy(ledstring_PWM.channel[0].leds, frame_0, BYTES_PER_FRAME_RING);
	memcpy(ledstring_PWM.channel[1].leds, frame_1, BYTES_PER_FRAME_RING);
	memcpy(ledstring_PCM.channel[0].leds, frame_2, BYTES_PER_FRAME_RING);
	// memcpy(ledstring_PCM.channel[0].leds, frame_2, BYTES_PER_FRAME_RING);
	// Not using these at the moment
	// memcpy(ledstring_PCM.channel[0].leds, data_0, BYTES_PER_FRAME_RING);
	// memcpy(ledstring_PCM.channel[1].leds, data_1, BYTES_PER_FRAME_RING);
	// Channel doesn't exist 
	// memcpy(ledstring_PCM.channel[1].leds, data_1, BYTES_PER_FRAME_RING); 
}

static void ctrl_c_handler(int signum)
{
    (void)(signum);
    printf("Termination signal detected\n");
    running = 0;
}

static void setup_handlers(void)
{
    printf("Set up signal handlers\n");
    struct sigaction sa = {
        .sa_handler = ctrl_c_handler,
    };
    sigaction(SIGINT, &sa, NULL);
    sigaction(SIGTERM, &sa, NULL);
}

static void setup_gpio_channel_pins(void)
{
	bcm2835_gpio_fsel(PWM_0_CHANNEL_0_PIN, BCM2835_GPIO_FSEL_OUTP);
	bcm2835_gpio_clr(PWM_0_CHANNEL_0_PIN);
	bcm2835_gpio_fsel(PWM_0_CHANNEL_1_PIN, BCM2835_GPIO_FSEL_OUTP);
	bcm2835_gpio_clr(PWM_0_CHANNEL_1_PIN);
	bcm2835_gpio_fsel(PWM_1_CHANNEL_0_PIN, BCM2835_GPIO_FSEL_OUTP);
	bcm2835_gpio_clr(PWM_1_CHANNEL_0_PIN);
	bcm2835_gpio_fsel(PWM_1_CHANNEL_1_PIN, BCM2835_GPIO_FSEL_OUTP);
	bcm2835_gpio_clr(PWM_1_CHANNEL_1_PIN);
	bcm2835_gpio_fsel(PCM_0_CHANNEL_0_PIN, BCM2835_GPIO_FSEL_OUTP);
	bcm2835_gpio_clr(PCM_0_CHANNEL_0_PIN);
	bcm2835_gpio_fsel(PCM_0_CHANNEL_1_PIN, BCM2835_GPIO_FSEL_OUTP);
	bcm2835_gpio_clr(PCM_0_CHANNEL_1_PIN);
}

static void enable_pwm_channel_0(void)
{
	bcm2835_gpio_clr(PWM_0_CHANNEL_1_PIN);
	bcm2835_gpio_clr(PWM_1_CHANNEL_1_PIN);
	bcm2835_gpio_set(PWM_0_CHANNEL_0_PIN);
	bcm2835_gpio_set(PWM_1_CHANNEL_0_PIN);
}

static void enable_pwm_channel_1(void)
{
	bcm2835_gpio_clr(PWM_0_CHANNEL_0_PIN);
	bcm2835_gpio_clr(PWM_1_CHANNEL_0_PIN);
	bcm2835_gpio_set(PWM_0_CHANNEL_1_PIN);
	bcm2835_gpio_set(PWM_1_CHANNEL_1_PIN);
}

static void enable_pcm_channel_0(void)
{
	bcm2835_gpio_clr(PCM_0_CHANNEL_1_PIN);
	bcm2835_gpio_set(PCM_0_CHANNEL_0_PIN);
}

static void enable_pcm_channel_1(void)
{
	bcm2835_gpio_clr(PCM_0_CHANNEL_0_PIN);
	bcm2835_gpio_set(PCM_0_CHANNEL_1_PIN);
}

int main(int argc, char *argv[])
{
	int count = 0;
    unsigned char led_array[BYTES_PER_FRAME];
    ws2811_return_t ret;
    size_t size;
	zmq_msg_t msg;
    setup_handlers();
    
    if ((ret = ws2811_init(&ledstring_PWM)) != WS2811_SUCCESS) {
        printf("ERROR: ws2811_init ledstring_PWM failed: %s\n", ws2811_get_return_t_str(ret));
        return ret;
    }
    if ((ret = ws2811_init(&ledstring_SPI)) != WS2811_SUCCESS) {
        printf("ERROR: ws2811_init ledstring_SPI failed: %s\n", ws2811_get_return_t_str(ret));
        return ret;
    }
    if ((ret = ws2811_init(&ledstring_PCM)) != WS2811_SUCCESS) {
        printf("ERROR: ws2811_init ledstring_PCM failed: %s\n", ws2811_get_return_t_str(ret));
        return ret;
    }
	if (!bcm2835_init()) {
		printf("ERROR: unable to init bcm2835 GPIO\n");
		return 1;
	}
	setup_gpio_channel_pins();

    void *aContext = zmq_ctx_new();        
    void *aSUB = zmq_socket(aContext, ZMQ_SUB );
    zmq_connect(aSUB,"tcp://127.0.0.1:5556"); 
    zmq_setsockopt(aSUB, ZMQ_SUBSCRIBE, "", 0);
    zmq_setsockopt(aSUB, ZMQ_LINGER, 0, 1);

	clock_gettime(CLOCK_MONOTONIC, &tstart);
    printf("Running\n");
    setbuf(stdout, NULL);
    while (running) {
        zmq_msg_init(&msg);
        zmq_msg_recv(&msg, aSUB, 0);
        size = zmq_msg_size(&msg);
        memcpy(led_array, zmq_msg_data( &msg ), BYTES_PER_FRAME);

        matrix_render(led_array + FRAME_0, led_array + FRAME_1, led_array + FRAME_2);
        enable_pwm_channel_0();
        if ((ret = ws2811_render(&ledstring_PWM)) != WS2811_SUCCESS) {
            fprintf(stderr, "ws2811_render ledstring_PWM failed: %s\n", ws2811_get_return_t_str(ret));
            break;
        }
        enable_pcm_channel_0();
        if ((ret = ws2811_render(&ledstring_PCM)) != WS2811_SUCCESS) {
            fprintf(stderr, "ws2811_render ledstring_PCM failed: %s\n", ws2811_get_return_t_str(ret));
            break;
        }
        //usleep(1000000 / 60);
        matrix_render(led_array + FRAME_3, led_array + FRAME_4, led_array + FRAME_5);
        enable_pwm_channel_1();
        if ((ret = ws2811_render(&ledstring_PWM)) != WS2811_SUCCESS) {
            fprintf(stderr, "ws2811_render ledstring_PWM failed: %s\n", ws2811_get_return_t_str(ret));
            break;
        }
        enable_pcm_channel_1();
        if ((ret = ws2811_render(&ledstring_PCM)) != WS2811_SUCCESS) {
            fprintf(stderr, "ws2811_render ledstring_PCM failed: %s\n", ws2811_get_return_t_str(ret));
            break;
        }
        //usleep(1000000 / 60);
        if (count % 100 == 0) {
			clock_gettime(CLOCK_MONOTONIC, &tend);
			printf("%.5f seconds: received [%d],%d\n", 
			    ((double)tend.tv_sec + 1.0e-9*tend.tv_nsec) - 
                ((double)tstart.tv_sec + 1.0e-9*tstart.tv_nsec), size, 
                count);
		}
        if (zmq_msg_close (&msg) != 0) {
            fprintf(stderr, "zmq_msg_close error");
            break;
        }
        count++;
    }

    zmq_close(aSUB);
    zmq_ctx_term(aContext);

    ws2811_fini(&ledstring_PWM);
    ws2811_fini(&ledstring_SPI);
    ws2811_fini(&ledstring_PCM);
	(void) bcm2835_close();
    printf ("Exit complete\n");
    return ret;
}
