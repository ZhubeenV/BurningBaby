import os, time, random, argparse, threading

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=120)
    ap.add_argument("--gpio", type=int, default=18)
    ap.add_argument("--brightness", type=int, default=160)
    ap.add_argument("--fps", type=int, default=60)
    ap.add_argument("--audio", action="store_true")
    ap.add_argument("--audio-min", type=int, default=20)
    ap.add_argument("--audio-max", type=int, default=90)
    return ap.parse_args()

def make_driver(count, gpio, brightness, fps):
    try:
        from rpi_ws281x import Adafruit_NeoPixel, Color
    except Exception:
        print("rpi_ws281x not available, using console SIM")
        def show_sim(pixels):
            if pixels:
                r = sum(p[0] for p in pixels)//len(pixels)
                g = sum(p[1] for p in pixels)//len(pixels)
                b = sum(p[2] for p in pixels)//len(pixels)
                print(f"SIM avg=({r},{g},{b}) n={len(pixels)}")
            time.sleep(1.0/max(1,fps))
        def cleanup_sim():
            pass
        return show_sim, cleanup_sim

    strip = Adafruit_NeoPixel(count, gpio, 800000, 10, False, brightness,
                              0 if gpio in (18,12) else 1)
    strip.begin()
    def show_hw(pixels):
        n = min(count, len(pixels))
        for i in range(n):
            r,g,b = pixels[i]
            strip.setPixelColor(i, Color(int(r), int(g), int(b)))
        strip.show()
        time.sleep(1.0/max(1,fps))
    def cleanup_hw():
        for i in range(count):
            strip.setPixelColor(i, 0)
        strip.show()
    return show_hw, cleanup_hw

def heat_to_color(h):
    t = (h*191)//255
    ramp = (t & 63) << 2
    if t > 128:   return (255, 255, ramp)
    if t > 64:    return (255, ramp, 0)
    return (ramp, 0, 0)

def fire_step(heat, cooling=55, sparking=120):
    n = len(heat)
    for i in range(n):
        heat[i] = max(0, heat[i] - random.randint(0, (cooling*10)//max(1,n) + 2))
    for k in range(n-1, 1, -1):
        heat[k] = (heat[k-1] + heat[k-2] + heat[k-2])//3
    if random.randint(0,255) < sparking:
        y = random.randint(0, min(7, n-1))
        heat[y] = min(255, heat[y] + random.randint(160,255))
    return [heat_to_color(h) for h in heat]

def audio_thread(folder, tmin, tmax, stop_evt):
    try:
        import pygame
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.6)
    except Exception:
        print("audio disabled")
        return
    if not os.path.isdir(folder):
        print("audio folder not found")
        return
    files = [f for f in os.listdir(folder) if f.lower().endswith((".mp3",".wav",".ogg"))]
    if not files:
        print("no audio files in ./audio")
        return
    while not stop_evt.is_set():
        wait_s = random.randint(tmin, tmax)
        for _ in range(wait_s):
            if stop_evt.is_set(): return
            time.sleep(1)
        path = os.path.join(folder, random.choice(files))
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() and not stop_evt.is_set():
                time.sleep(0.1)
        except Exception as e:
            print("audio error:", e)

def main():
    args = parse_args()
    show, cleanup = make_driver(args.count, args.gpio, args.brightness, args.fps)
    heat = [0]*args.count
    stop_evt = threading.Event()
    if args.audio:
        t = threading.Thread(target=audio_thread, args=("audio", args.audio_min, args.audio_max, stop_evt), daemon=True)
        t.start()
    try:
        while True:
            pixels = fire_step(heat)
            show(pixels)
    except KeyboardInterrupt:
        pass
    finally:
        stop_evt.set()
        cleanup()

if __name__ == "__main__":
    main()
