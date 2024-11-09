# packetbeeps
- unnamed project for sniffing traffic and making some art
- a chance to improve my rust, network configuration, sys admin skills....
- Hardware used: Raspi3b (2015), passive buzzer  KY-006
- Current status: works nicely with python

# initial breakdown by chatgpt

---

### **High-Level Missions**
1. **Packet Sniffer Setup**  
   Capture and process network packets from your local network.
   
2. **Signal Generator**  
   Convert packet data into meaningful signals (beeps, tones, or LED patterns).

3. **Artistic Output**  
   Translate the signals into a tangible medium (sound or light art).

---

### **Detailed Breakdown**
#### ****Mission 1: Packet Sniffer Setup**
- **Submissions**:**
  1. Configure your router for port mirroring or packet forwarding to the Pi.
  2. Set up packet capture on the Raspberry Pi.
  3. Parse the captured packets to extract meaningful information (e.g., protocol type, size, or direction).
  
- **Technologies**:
  - **Library**: Use `libpcap` (or its Rust wrapper, `pcap`).
  - **Tools**: Wireshark for initial packet exploration.
  - **Output**: A simple log file showing the number and type of packets received.

---

#### **Mission 2: Signal Generator**
- **Submissions**:
  1. Create a mapping of packet attributes (e.g., TCP vs. UDP, packet size) to sounds or LED signals.
  2. Develop a tone/beep generator to produce audio output based on the mapped values.
  3. For LEDs, interface with GPIO to light up or flash patterns.

- **Technologies**:
  - **Audio**: 
    - For Rust: Use `rodio` for audio playback.
    - For Python (if you prefer): Use `pygame` for simple tone generation.
  - **GPIO for LEDs**:
    - For Rust: Use `rppal` (Raspberry Pi Peripheral Access Library).
    - For Python (alternative): Use the `RPi.GPIO` or `gpiozero` libraries.

---

#### **Mission 3: Artistic Output**
- **Submissions**:
  1. Combine audio and LED signals into a synchronized art piece.
  2. Create dynamic adjustments (e.g., increasing tempo with higher traffic).
  3. Add filters or toggles to control which packets influence the output.

- **Technologies**:
  - **Multithreading** (for real-time sync): Use Rust’s powerful async ecosystem or Python’s `asyncio`.

---

### **Feasibility of Using Rust on Raspberry Pi 3**
Rust is a **great choice** for this project! Here’s why and how:
- **Advantages**:
  1. **Performance**: Rust is fast and can handle real-time processing better than Python.
  2. **Safety**: Rust’s memory safety makes it less error-prone than C, and it avoids segmentation faults.
  3. **Fun**: This is an excellent opportunity to learn Rust while working on a tangible, creative project.

- **Challenges**:
  - The Raspberry Pi 3 isn’t very powerful, but with Rust’s performance optimization, it should handle this project well.
  - Learning curve: If you’re new to Rust, some concepts (e.g., lifetimes, borrowing) might require a bit of practice.

- **Rust Tools & Libraries**:
  - **Packet Capture**: Use the `pcap` crate.
  - **Audio Output**: Use the `rodio` or `bevy_audio` crates.
  - **GPIO for LEDs**: Use `rppal`.
  - **Cross-Compilation**: Install the Rust toolchain for ARM architecture (`arm-unknown-linux-gnueabihf`).

---

### Suggested Milestones
1. **Explore Packet Data**  
   - Use `Wireshark` to examine packets locally.  
   - Run a simple Rust program with `pcap` to capture packets on the Raspberry Pi.  

2. **Generate Audio Beeps**  
   - Write a Rust script that plays tones based on dummy packet input.

3. **Integrate LEDs**  
   - Use `rppal` to toggle LEDs via GPIO. Map packet data to LED patterns.

4. **Optimize for Real-Time**  
   - Fine-tune packet processing to ensure smooth signal generation and avoid overloading the Pi.

5. **Polish the Art**  
   - Experiment with packet mappings and refine the audio/LED interplay.

---

### Tools You'll Need
1. **For Development**:
   - Install Rust: Use `rustup` (`curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`).
   - Cross-compilation toolchain: `arm-unknown-linux-gnueabihf`.
2. **Hardware**:
   - Raspberry Pi 3 with Raspbian OS.
   - Breadboard, LEDs, resistors, and jumper wires (optional for LED art).
3. **For Packet Capture**:
   - `tcpdump` (pre-installed on most Linux systems) for testing packet forwarding.

---
