# IS Encrypted Communication Infrastructure
Information Security Lab - Communication infrastructure using the AES cryptosystem for traffic encryption between two nodes.

Requirements:

1. We consider a node KM (key manager) which owns 2 keys on 128 bits: K and K'. K' will be used for encrypting K. By convention, the initialization vector has a fixed value, known by default by both A and B. Same for K'.
2. To begin a communication session, A sends a message to B in which it communicates the mode of operation, either CBC or OFB, asking KM for the encryption key at the same time. KM will randomly generate K and will encrypt it using AES and key K'. After A receives the resulting key from KM, it will then send it to B. Both A and B will decrypt it in order to start the communication. B will be the first one to send A a signal.
3. After receiving the signal from B (regarding the beginning of message exchange), A starts to send B the content of an encrypted file, using the selected mode of operation. B will decrypt the received blocks and will display the result.

Demo: https://www.youtube.com/watch?v=LhrI5sAf5pA&feature=youtu.be
