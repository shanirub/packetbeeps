import time
import platform
from scapy.all import sniff

stop_sniffing = False
play_buzzer = False
buzzer = None

def is_raspberry_pi():
    try:
        with open('/proc/device-tree/model', 'r') as f:
            model = f.read()
            return 'Raspberry Pi' in model
    except FileNotFoundError:
        return False

def stop_filter(packet):
    global stop_sniffing
    return stop_sniffing

def calculate_tone(protocol, sport, dport, packet_size, ttl):
    # Map protocol to a base note
    protocol_map = {
        "TCP": 0,  # C4
        "UDP": 1,  # D4
        "ICMP": 2  # E4
    }
    base_note = protocol_map.get(protocol, 0)  # Default to C4

    # Map source port and destination port to variations
    tone_offset = (sport + dport) % 8  # Map to one of 8 tones

    # Scale tone by packet size
    size_offset = (packet_size // 100) % 8  # Larger packets shift notes

    # Adjust for TTL
    ttl_shift = (ttl // 32) % 8  # Normalize TTL to a range

    # Calculate final tone index
    tone_index = (base_note + tone_offset + size_offset + ttl_shift) % 8

    return tone_index


def process_packets(packet_batch):
    global buzzer
    print(f"Processing {len(packet_batch)} packets...")
    for packet in packet_batch:
        # Example: Extract properties and play sound
        protocol = packet.sprintf("%IP.proto%") if packet.haslayer('IP') else "Unknown"
        sport = getattr(packet, 'sport', 0)
        dport = getattr(packet, 'dport', 0)
        size = len(packet)
        ttl = getattr(packet, 'ttl', 64)

        # Send packet data to sound generator
        tone_index = calculate_tone(protocol, sport, dport, size, ttl)
        print(f"Playing tone index: {tone_index}")

        if play_buzzer and buzzer:
            buzzer.play_note(tone_index)

# Tone mapping logic
def packet_callback(packet):
    protocol = packet.sprintf("%IP.proto%")  # TCP, UDP, etc.
    sport = packet.sport if hasattr(packet, "sport") else 0
    dport = packet.dport if hasattr(packet, "dport") else 0
    size = len(packet)
    ttl = packet.ttl if hasattr(packet, "ttl") else 64

    tone_index = calculate_tone(protocol, sport, dport, size, ttl)
    print(f"Playing tone index: {tone_index}")

def main():
    global stop_sniffing
    global buzzer
    global play_buzzer
    play_buzzer= is_raspberry_pi()

    if play_buzzer:
        from buzzer import Buzzer
        buzzer = Buzzer()

    print(f"Running on raspi: {play_buzzer}. buzzer: {buzzer}")
    print("Starting packet sniffing... Ctrl+C to stop")
    try:
        while not stop_sniffing:
            print(f"stop sniffing is {stop_sniffing}")
            # Sniff 10 packets at a time
            packets = sniff(count=10, timeout=5, stop_filter=stop_filter)  # Timeout ensures it doesn't hang if no packets are captured
            if packets:
                process_packets(packets)
            else:
                print("No packets captured in this cycle.")
                # Add a sleep to allow system to handle interrupt
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt detected, stopping...")
        stop_sniffing = True


    print("Exiting gracefully.")

if __name__ == "__main__":
    main()


"""
parallel option

import threading
from queue import Queue
from scapy.all import sniff

def process_packets(packet_queue):
    while True:
        packets = packet_queue.get()
        if packets is None:  # Exit signal
            break
        for packet in packets:
            # Tone processing logic here
            tone_index = calculate_tone("TCP", 12345, 80, 512, 64)  # Placeholder
            print(f"Playing tone: {tone_index}")
            # play_sound(tone_index)
        packet_queue.task_done()

def main():
    packet_queue = Queue()
    processor_thread = threading.Thread(target=process_packets, args=(packet_queue,))
    processor_thread.start()

    print("Starting packet sniffing...")
    try:
        while True:
            packets = sniff(count=10, timeout=5)
            if packets:
                packet_queue.put(packets)
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        packet_queue.put(None)  # Signal the processor thread to exit
        processor_thread.join()

if __name__ == "__main__":
    main()

"""