# Week 5 — Report  
## Why CRC Works: Error Detection in Simple Terms

---

## How CRC Represents Data

CRC treats a binary message as a mathematical object called a polynomial.

For example:

$$
1101 \leftrightarrow x^3 + x^2 + 1
$$

This may look abstract, but the idea is simple:
- Each bit becomes a term  
- The position of the bit gives the power of $x$  

This representation allows us to use math (specifically division) to detect errors.

---

## How CRC Encoding Works

To send a message safely, CRC adds a few extra bits.

The process works like this:

1. Take the original message  
2. Add some zeros to the end  
3. Divide the result by a fixed pattern (called the generator)  
4. Take the remainder and attach it to the message  

The final message is sent over the network.

The key idea is:
- The final message is always divisible by the generator  

This property is what allows the receiver to detect errors later.

---

## How Errors Are Detected

At the receiver side:
- The system divides the received message by the same generator  
- If the remainder is 0 → the message is accepted  
- If the remainder is not 0 → an error is detected  

If an error happens during transmission, the message changes. This breaks the divisibility property.

An error is only missed if the error pattern is also divisible by the generator. Good generators are chosen so this almost never happens.

---

## What Errors CRC Can Detect

CRC is very strong at detecting errors.

It can always detect:
- Any single-bit error  
- Any short burst error (up to a certain length)  

It can also detect most larger errors with very high probability.

For example:
- CRC-32 (used in Ethernet and WiFi) misses errors with probability about:

$$
2^{-32}
$$

This is extremely small, so in practice CRC catches almost all errors.

---

## Why CRC Works So Well

The strength of CRC comes from two ideas:

1. It turns error detection into a math problem (division)  
2. The generator is carefully chosen to avoid common error patterns  

Because of this, most errors will produce a nonzero remainder and be detected.

---

## CRC in Real Networks

CRC is used at the link layer in real systems.

For example:
- Ethernet frames include a CRC-32 value  
- WiFi frames also include a CRC-32 value  

When a device receives a frame:
- It checks the CRC  
- If there is an error, the frame is simply discarded  

There is no attempt to fix the error at this stage.

---

## Why Networks Prefer Detection Over Correction

There are two main approaches to handling errors:
- Detect errors and resend the data  
- Correct errors directly  

In networking, detection is usually preferred.

Reasons:
- It uses less extra data (more efficient)  
- Retransmission is cheap in packet networks  
- Error correction adds complexity and overhead  

So the common strategy is:
- Use CRC to detect errors  
- Let higher layers (like TCP) handle retransmission  

---

## Reflection

Before learning this, I thought error correction would always be better. It seems more powerful because it can fix mistakes.

However, CRC shows that detecting errors is often enough. It is simple, fast, and very reliable.

The design choice is not about being perfect. It is about being efficient.

---

## Generative AI Usage

I used ChatGPT to help organize this report and explain CRC in simpler terms.

Specifically:
- It helped simplify the explanation of polynomial representation  
- It clarified how CRC detects errors using division  
- It helped structure the report in a clear, logical way  
