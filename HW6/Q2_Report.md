# System Overview

In our HoneyWords system, it includes 3 main actors. 

- Users (Clients)

  They can choose to perform one of two actions:

  1.  Create an account
  2.  Authenticate an account

- Front-end server
  It is responsible for the storage of user password hashes as well as their unique salt values. 
  It is also the main communication platform with the users and the HoneyChecker.

- HoneyChecker
  It helps to store the index of the real password hash in the password dictionary maintained by the front-end server.
  Using this index, it is responsible for validating passwords, where it will distinguish valid passwords from honeywords.

## System Architecture Design

![System_Architecture_Diagram](https://raw.githubusercontent.com/Pillowkoh/51.502-System-Security/main/HW6/images/System_Architecture_Diagram.png)

# How it works:

This section will give details on each individual process of the implemented HoneyWords System. Please refer to the video for demonstration of the entire process. (Note: We will use "clients" interchangeably with "users".) 

## 1. Initialisation of Server

During the initialisation phase of the front-end server, port number 8080 and 8090 are assigned as the TCP connection ports for client-server and server-HoneyChecker connections respectively. The front-end server will actively listen for any request made by the clients and handle them accordingly.

Server:

![Server_Init](https://raw.githubusercontent.com/Pillowkoh/51.502-System-Security/main/HW6/images/Server_Init.png)

## 2. Account Creation

In the account creation stage, the client would be required to provide a (user_id, password) pair to the front-end server. The front-end server will create a new unique salt for this user_id and create a salted hash for the password provided. Along with the salted hash, the front-end server also generates a list of hashes for honeywords (decoy passwords). The salted hash of the original password will be appended to this list of honeyword hashes and the list is randomly shuffled. The user_id and this list of hashes is stored as a (key, value) pair in a dictionary within the local storage of the front-end server. The index of the salted hash for the original password will be sent over to the HoneyChecker along with the user_id to be stored within the local storage of the HoneyChecker.

Client:

![Client_Creation](https://raw.githubusercontent.com/Pillowkoh/51.502-System-Security/main/HW6/images/Client_Creation.png)

Server:

![Server_Creation](https://raw.githubusercontent.com/Pillowkoh/51.502-System-Security/main/HW6/images/Server_Creation.png)

## 3. Account Authentication

In this phase, the client will provide a (user_id, password) pair to the front-end server for account authentication. There will be 4 various outcomes as described in detail below:

### Case 1 - (Incorrect User ID)

In the first case, the front-end server checks its own local database for the user_id provided by the client and denies access to the client as the user_id provided is invalid.

Client:

![Client_Invalid_User](https://raw.githubusercontent.com/Pillowkoh/51.502-System-Security/main/HW6/images/Client_Invalid_User.png)

Server:

![Server_Invalid_User](https://raw.githubusercontent.com/Pillowkoh/51.502-System-Security/main/HW6/images/Server_Invalid_User.png)

### Case 2 - (Correct User ID & Password)

In the second case, the front-end server checks its own local database for the user_id provided by the client. After verifying that the user_id is valid, it will retrieve the unique salt value of the user and generate a salted password hash based on the password provided by the client. Upon validation of the salted password hash with its local database, it will send the index of this hash to the HoneyChecker to verify if the salted password hash corresponds to the actual password. The HoneyChecker checks this index against its own database and sends back a verification response to the front-end server. The front-end server will then authenticate the client.

Client:

![Client_Successful](https://raw.githubusercontent.com/Pillowkoh/51.502-System-Security/main/HW6/images/Client_Successful.png)

Server:

![Server_Successful](https://raw.githubusercontent.com/Pillowkoh/51.502-System-Security/main/HW6/images/Server_Successful.png)

### Case 3 - (Correct User ID & Incorrect password)

The process for case 3 is similar to that of case 2. However, the salted password hash that is generated will not be able to pass the verification process by the front-end server. On failure of this verification process, the front-end server will terminate the authentication process and deny access to the client.

Client:

![Client_Invalid_Pwd](https://raw.githubusercontent.com/Pillowkoh/51.502-System-Security/main/HW6/images/Client_Invalid_Pwd.png)

Server:

![Server_Invalid_Pwd](https://raw.githubusercontent.com/Pillowkoh/51.502-System-Security/main/HW6/images/Server_Invalid_Pwd.png)

### Case 4 - (Correct User ID & Honeyword Password)

The process for case 4 is similar to that of case 2. However, the difference is that the salted password hash will fail during the verification process by the HoneyChecker. On failure, the HoneyChecker returns a False value to the front-end server which will in turn trigger an alert.

Client:

![Client_Honeyword](https://raw.githubusercontent.com/Pillowkoh/51.502-System-Security/main/HW6/images/Client_Honeyword.png)

Server:

![Server_Honeyword](https://raw.githubusercontent.com/Pillowkoh/51.502-System-Security/main/HW6/images/Server_Honeyword.png)

# Analysis of System Security

In our implementation of the HoneyWords system, we introduced two main components:

1. Salted Password Hashes
2. Separated Database (Front-end Server and HoneyChecker)

## Salted Password Hashes

This is a technique used to store passwords securely by adding a random value (known as a salt) to the password before hashing it. The resulting salted hash is then stored in the database. The main advantages of using salted password hashes are:

1. **Increased security:** 

   Salted password hashes provide increased security compared to storing passwords in plain text or using unsalted hashes. The salt makes it much harder for attackers to use precomputed hash tables or rainbow tables to crack the passwords.

2. **Prevents identical passwords from having the same hash:**

   If two users have the same password, and that password is not salted, then their password hashes would be identical. This can be exploited by attackers who can use the same password hash to access multiple accounts. By using salted hashes, each user's password hash will be unique, even if they have the same password.

3. **Difficult to reverse-engineer:** 

   Salted password hashes are difficult to reverse-engineer because the salt adds an extra layer of complexity. An attacker would need to know the salt used for each user's password, as well as the hashing algorithm used, in order to reverse-engineer the password from the hash.

## Separated Database (Front-end Server and HoneyChecker)

1. **Improved security:** 

   Separating databases can help to increase security by reducing the potential impact of security breaches. For example, if one database is compromised, the other databases may still be secure. In this HoneyWords System, it means that an attacker would have to gain access to both databases in order to crack the user password.

2. **Enhanced data organization:** 

   Separating databases can help you to organize your data more effectively. By separating data by type or function, you can reduce complexity and make it easier to manage and access the data.

## Vulnerabilities

In our implementation of the HoneyWords System, we lack security control against eavesdropping attacks. Such attacks are usually performed through Man-in-The-Middle (MiTM) techniques which includes IP Sniffing and Spoofing. To login to our system successfully without triggering alarms, we can follow the attack tree drawn below:

### Attack Tree

![Attack Tree](https://raw.githubusercontent.com/Pillowkoh/51.502-System-Security/main/HW6/images/Attack_Tree.png)

# Security Control

To combat MiTM attacks, we propose 3 different defense mechanisms. Namely:

1. **Public-Key Infrastructure (PKI):** 

   This is a system used to create, manage, and distribute digital certificates and public keys to users or devices in a network. PKI can help prevent MiTM attacks by verifying the authenticity of the communication between the client and the server. When two devices communicate using PKI, they exchange digital certificates that include public keys, which are verified by a trusted third-party certification authority (CA) to ensure that they belong to the intended parties. This ensures that the communication is secure and not intercepted by an attacker.

2. **Multi-Factor Authentication (MFA):** 

   This is a security mechanism that requires users to provide two or more forms of authentication to access a network or device. Typically, this involves a combination of something the user knows (such as a password), something the user has (such as a token or smart card), or something the user is (such as biometric data like fingerprints). MFA helps prevent MiTM attacks by making it more difficult for an attacker to impersonate a legitimate user and gain access to the network or device.

3. **Firewall:** 

   This is a network security system that monitors and controls incoming and outgoing network traffic based on predetermined security rules. A firewall can help prevent MiTM attacks by filtering out unauthorized traffic and blocking suspicious connections that could be used by an attacker to intercept or manipulate communication between two parties.



These proposed security control measures* can be added into our HoneyWords System easily as shown in the System Architecture Diagram below:
(*Security control measures are highlighted in the yellow blocks)

### Improved System Architecture Diagram

![System_Architecture_Diagram_Secure](https://raw.githubusercontent.com/Pillowkoh/51.502-System-Security/main/HW6/images/System_Architecture_Diagram_Secure.png)