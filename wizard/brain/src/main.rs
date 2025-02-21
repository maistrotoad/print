#![no_std]
#![no_main]

// Pull in the panic handler from panic-halt
use panic_halt as _;

use arduino_hal::spi;

use arduino_hal::prelude::*;

use ws2812_spi as ws2812;

use crate::ws2812::prerendered::Ws2812;
use smart_leds::{SmartLedsWrite, RGB8};



#[arduino_hal::entry]
fn main() -> ! {
    let dp = arduino_hal::Peripherals::take().unwrap();
    let pins = arduino_hal::pins!(dp);
    let mut serial = arduino_hal::default_serial!(dp, pins, 57600);

    // Create SPI interface.
    let ( spi, _) = arduino_hal::Spi::new(
        dp.SPI,
        pins.d13.into_output(),
        pins.d11.into_output(),
        pins.d12.into_pull_up_input(),
        pins.d10.into_output(),
        spi::Settings::default(),
    );

    const NUM_LEDS: usize = 108;

    let mut output_buffer = [0; 20 + (NUM_LEDS * 12)];
    let mut data: [RGB8; NUM_LEDS] = [RGB8::default(); NUM_LEDS];
    let empty: [RGB8; NUM_LEDS] = [RGB8::default(); NUM_LEDS];
    let mut ws = Ws2812::new(spi, &mut output_buffer);
    loop {

        for i in 0..NUM_LEDS/3 {
            let start = i*3;
            data[start] = RGB8 {
                r: 0,
                g: 0,
                b: 0x5,
            };
            data[start+1] = RGB8 {
                r: 0,
                g: 0x5,
                b: 0,
            };
            data[start+2] = RGB8 {
                r: 0x5,
                g: 0,
                b: 0,
            };
        }

        ws.write(data.iter().cloned()).unwrap();
        arduino_hal::delay_ms(1000 as u16);
        ws.write(empty.iter().cloned()).unwrap();
        arduino_hal::delay_ms(1000 as u16);
    }

}