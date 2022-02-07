![License: MIT](https://img.shields.io/badge/License-MIT-%23E6F0FD)
![Status: Finished](https://img.shields.io/badge/Status-Finished-%235d6d91)



# Password manager

Password manager is a piece of software that allows its users to safely store login credentials to other services. This project is a very simple and definitely not perfect implementation of it, it was made to showcase different approaches to storing passwords and you are definitely better off using something like Bitwarden. 

I divided this project to two sections: introduction and development of the application. The first one is way longer since in the documentation I will go into details of encryption vs hashing, different algorithms and try to answer some questions that came up while I was studying the basics.



## The project

This project is a password manager that was created to showcase the use of encryption in practice. By any means it is not a tool that you should use on everyday basis as it's only made to be a proof of concept. I based the functionality on Bitwarden: the user is able to add credentials and retrieve them, everything encrypted with a master password as the key. The user can also choose to generate a [passphrase](https://protonmail.com/blog/protonmail-com-blog-password-vs-passphrase/) instead of a random string of characters. For encryption I am using Fernet (AES symmetric algorithm + SHA256 for authentication) from Python's cryptography library. The requirements can be found in the requirements.txt file, please install them before starting the project.



### Quickstart

1. Install the requirements

   ```
   pip install requirements.txt
   ```

2. Start the application

   ```
   python main.py
   ```

   

## Introduction

At the very beginning of making this project, I was confused about a lot of things related to password security. Not only by my own misunderstanding of the topic but also some weird explanations of them I got from people I know. Let's start from the square one and up the ladder of security, we start at storing credentials as plain text - do not do it. It's the worst thing you can do, security is compromised every time someone has a look at them and that can happen in many ways. Now that being said, let's move towards two ways in which you can secure data: encryption and hashing. The amount of people that I've encountered who don't understand the distinction is concerning so in the two following sections I will explain how they work.



![Comparison](https://imgur.com/KWkdqPa.png)



### Hashing

**Hashing** is a one-way of securing information, it means that once something is hashed, it cannot go back to its original form. It's a nice way of securing passwords for example. Let's imagine a situation like that: user visits a login page and sends a request with a form containing their password. We want to check if its correct so all we have to do is hash it and compare to the hash in the database. Sounds good right? We don't store the original password and everything is safe. Until we get a rainbow table attack and it's not. This is why we introduce something called salt. **Salt** is a way of mixing up the hash in an unique way that slows down attacks quite significantly. Without salt, two the same passwords look the same when hashed, with salt they look different. If  the attacker would hash the 10M most common passwords and compare them to the ones in our database, they would have to do so for each unique salt not the whole table at the same time. 

Now let's move into how hashing works in practice, how can one hash a piece of text? There is a lot of different hashing algorithms available, let's talk about the most known and used ones. **SHA** is something you probably have heard about if you ever read anything about hashing, it stands for Secure Hashing Algorithm and has a few versions and the ones you will most commonly encounter are **SHA-1 and SHA-2**. According to Wikipedia, "Since 2005, SHA-1 has not been considered secure against well-funded opponents; as of 2010 many organizations have recommended its replacement. "

SHA-2 had some important changes from the past version.  It is a family of two similar hash functions, with different block sizes, known as SHA-256 and SHA-512. The main difference is between the sizes, the former uses 32-byte words where as the latter uses 64-byte words. 

The algorithm is good and pretty much the standard but when it comes to passwords, we might want to consider one additional thing that is the speed of hashing them. You might think that we want our algorithms to be fast, wrong! The previous algorithms I mentioned were designed to be fast since there is no reason for generic hashes to be slow, you don't want any delay in validating a signature for example. When it comes to passwords we want to slow down possible attacks as much as possible, and it's getting harder and harder with the more computational power we obtain. This is where password hashes enter the game and we meet another player called Bcrypt. **Bcrypt** is a password hashing function, based on the Blowfish cipher presented at USENIX 1999. The best part is - it can be as slow as you want it to be. Blowfish is a symmetric-key block cipher and was created to have additional computational cost as the hardware improved. Bcrypt uses Blowfish internally, it is not an encryption algorithm since the output is not reversible, and it allows you to pick the cost based on how important the speed/security tradeoff is. 

#### In practice:

- *Examples of use:*
  - [Bcrypt with Python]()
- *Hashing algorithms:*
  - [Cryptography: Hash functions](https://www.youtube.com/watch?v=KqqOXndnvic) by MIT
  - [SHA - Secure Hashing Algorithm](https://www.youtube.com/watch?v=DMtFhACPnTY&t=1s) by Computerphile
  - [Hashing algorithms and security](https://www.youtube.com/watch?v=b4b8ktEV4Bg) by Computerphile



## Encryption

**Encryption** is a way of securing digital data by transforming it into an unreadable code that can be decrypted using a key. One of the most famous examples of encryption include [Enigma](https://www.youtube.com/watch?v=ASfAPOiq_eQ) and I think it's the best way to imagine how it works and its purpose. Encryption goes two ways and is usually used when the original information needs to be restored in the future. The history of encryption goes far back into ancient Rome, over two thousands years ago Caesar needed a way to send important documents to its troops in the field and developed a method called a substitution cipher. You can read more about encryption's history and use in [this amazing document.](https://www.giac.org/paper/gsec/1555/history-encryption/102877#:~:text=The%20first%20use%20of%20encryption,method%20called%20the%20substitution%20cipher.) 

Now concerning the standards of encryption I will start with symmetric-key algorithms that I will involve in the project. The first one I want to mention is **Triple DES** which used to be the first common standard for encryption back in the day. It was based on the first **DES** algorithm that quickly was found to be vulnerable to attacks but important to the advancement of cryptography. 3DES was an attempt to enhance it by applying the DES cipher three times which made it believed to be practically secure. It was first published in 1995 and is no longer considered adequate considering modern computer power and cryptography techniques. Although it's still used in banking and some businesses, the time of its retirement is coming in 2023 as announced by NIST in its [2019 draft guidance.](https://csrc.nist.gov/CSRC/media/Publications/sp/800-131a/rev-2/draft/documents/sp800-131Ar2-draft.pdf)

The newer, safer standard that is used by most nowadays is called **AES (Advanced Encryption Standard)**. It is used by the governments, security organizations and normal companies. NIST selected three members of the Rijndael block cipher family for its purpose: all with a block of 128 bits but three different key lengths,  128, 192 and 256 bits. AES was first published in 1998 and is included in the [ISO](https://en.wikipedia.org/wiki/International_Organization_for_Standardization)/[IEC](https://en.wikipedia.org/wiki/International_Electrotechnical_Commission) [18033-3](https://en.wikipedia.org/wiki/List_of_International_Organization_for_Standardization_standards,_18000-19999) standard.

There is plenty of different technologies to choose from nowadays and I'd also like to mention a few others that are also commonly used. Aside of the symmetric-key encryption we also have asymetric-key type of it that is used for one way communication. 

Blowfish is an another symmetric-key algorithm that I already mentioned once already under the hashing part of the document. Alongside AES, it was one of the algorithms made to replace 3DES. It breaks down data into 64-bit blocks and encrypts them individually. Blowfish was a predecessor to Twofish, Bruce Schneier's entry into the competition that produced AES. 

Assymetric-key algorithms like RSA (Rivest–Shamir–Adleman, named after its creators) are used for secure data transmissions and use two keys, a public and a private one, to encrypt and decrypt information.



![](https://twilio-cms-prod.s3.amazonaws.com/original_images/19DfiKodi3T25Xz7g9EDTyvF9di2SzvJo6JebRJaCN-1P_c1fMqGtrAyZzxGGucG0bcmR8UwNes-gS)



Many protocols like TLS or SSL rely on asymmetric cryptography. It is popular anywhere where a secure connection needs to be established like web browsers or in software that needs to validate a digital signature. For the purpose of the project this kind of technology is not needed but I still wanted to mention it.



## Standards of Security

For this project I focused on following official NIST guidelines on creating passwords. One of the additional features that I included is the choice between generating a standard password (mix of characters) and a passphrase. Passphrases can be especially useful because they are easy to remember (user doesn't always need a password manager to log-in) and they also are sufficiently long. As the recent research had shown, [length of the password is much more important than it's complexity.](https://pages.nist.gov/800-63-3/sp800-63b.html#appA) The password vault is properly encrypted using [current standards](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/archived-crypto-projects/aes-development) and uses the master password as a key.



## Additional Resources

- [Cryptography I by Stanford University](https://www.coursera.org/learn/crypto#syllabus)
- [NIST on Cryptography](https://www.nist.gov/cryptography)

