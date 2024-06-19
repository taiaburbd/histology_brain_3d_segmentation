
# Developer Guide

This guide is designed to help you set up your development environment for working with the ccub and GPU servers at the University of Burgundy.

## Prerequisites

- **Visual Studio Code** is recommended as the primary editor.
- Ensure you have **SSH access** and necessary permissions for the servers listed in this guide.

## Setup Instructions

### 1. Install Visual Studio Code (VS Code)

Download and install VS Code from [here](https://code.visualstudio.com/).

### 2. Install the Remote Explorer Add-on

Install the Remote Explorer extension to easily manage your remote SSH connections in VS Code. Get the extension from the [Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=ms-vscode.remote-explorer).

### 3. Configure SSH

Set up your SSH configuration to easily connect to the ccub and GPU servers. Edit your SSH config file located at `~/.ssh/config` and add the following configurations:

```bash
# Configuration for ccub
Host CCUB
    HostName ssh-ccub.u-bourgogne.fr
    User tr855969 # replace your user UB user name
    IdentityFile ~/.ssh/id_rsa
    ForwardAgent yes
    ForwardX11 yes
    ForwardX11Trusted yes
    ServerAliveCountMax 300
    ServerAliveInterval 100
    TCPKeepAlive yes

# Configuration for GPU
Host GPU
    HostName webern49.u-bourgogne.fr
    User tr855969
    IdentityFile ~/.ssh/id_rsa
    ForwardAgent yes
    ForwardX11 yes
    ForwardX11Trusted yes
    ServerAliveCountMax 300
    ServerAliveInterval 100
    TCPKeepAlive yes
    ProxyJump CCUB
```

### 4. SSH Auto-login

Configure SSH auto-login if required by your workflow. This typically involves setting up SSH keys and adding them to the `ssh-agent`.

a. Access via Terminal to CCUB: 

```bash
ssh CCUB 
```

![Alt text](images/example.png)

b. ACCESS via Terminal to GPU:
after success full login gpu 


```bash
ssh GPU
```
### 5. Create and Manage Conda Environments

Use the following commands to create and activate a new Conda environment:

```bash
conda create -n env_ngmm python=3.10
conda activate env_ngmm
```

Deactivate the environment when done:

```bash
conda deactivate
```

### 6. Additional Configuration
This configure for the CCUB server
Add custom configurations to your `.kshrc` and `.profilerc` as needed for your development environment.

#### add in `.kshrc`:

```bash
. /usr/ccub/bin/newprompt
export COLUMNS=180
module load 'pytorch/1.11.0/cuda/11.3.1/gpu'
```
#### add in `.bashhrc`:

```bash
echo 'Now using bash'

export nnUNet_raw="/user1/ngmm/tr855969/Desktop/Taiabur/ngmm-nnunet/dataset/nnUNet_raw_data"
export nnUNet_preprocessed="/user1/ngmm/tr855969/Desktop/Taiabur/ngmm-nnunet/dataset/nnUNet_preprocessed"
export nnUNet_results="/user1/ngmm/tr855969/Desktop/Taiabur/ngmm-nnunet/dataset/nnUNet_results"

source /etc/profile.d/modules.sh
module load 'pytorch/1.11.0/cuda/11.3.1/gpu'
```

### 7. Conda Initialization

Ensure Conda is properly initialized in your shell environment by following the setup in your `.kshrc` or `.profilerc`.

## Conclusion

Following these steps should prepare your development environment for effective and efficient project work. Adjust configurations as necessary based on your specific project requirements and server configurations.
