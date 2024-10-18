**idlegame** is a lightweight, terminal-based idle game designed to be played during downtime, such as while waiting for software builds or during short work breaks. It combines simple, casual gameplay with learning opportunities, particularly for those interested in command-line interfaces like zsh. Here's a breakdown of its features, installation steps, and how to play:

---

### **Installation**
To install **idlegame**, you can easily do so using Python's package manager, `pip`. All it takes is the following command in your terminal:

```bash
pip install idlegame
```

This command will download and install the game on your system, making it ready to play in just seconds.

---

### **Usage**
Once installed, simply launch the game by typing:

```bash
idlegame
```

After running this command, you’ll be immersed in the idle game environment.

---

### **Features**
- **Simplicity**: The game is incredibly easy to get started with. It's designed to be intuitive, making it accessible for anyone familiar with basic terminal commands.
- **Casual Play**: Perfect for short breaks. You can step away from coding, and still have something fun to do without requiring too much focus.
- **Offline Progress**: Even when you’re not actively playing, your in-game units (nanobots) continue to perform tasks.
- **Auto-Saving**: The game automatically saves progress, ensuring you never lose your current status.

---

### **Gameplay Overview**
In **idlegame**, you play by interacting with a zsh-like terminal environment. Commands you use within the game are valid zsh commands, making it a learning tool for mastering the terminal as well as a fun distraction.

- **Nanobots**: These are the primary units in the game. You create and script them to carry out various tasks like mining for resources or defending against invasions.
  
For example, you can create a nanobot using the `nano` command, script its logic, and let it work for you while you're idle.

### **Example Quickstart**
In the game, you might start off by receiving a resource called a "nano core," which is used to create nanobots. Here's a typical command sequence to create a nanobot:

```zsh
bb@idlegame % nano --name mine&defend -y
Write the logic for your nanobot (type 'done' on a new line to finish):
idle mine
on invasion defend
done
Nanobot 'mine&defend' created!
```

This creates a bot that will mine for resources when idle and defend your base in case of invasion.

---

### **Getting Unstuck**
If you ever find yourself confused or stuck, **idlegame** includes a built-in help command:

```zsh
man
```

This command provides a manual explaining the game’s mechanics and available commands. If you need more specific help about a particular command, you can type `man [command]` to get more detailed information.

---

### **Contributing**
The game is open-source and welcomes contributions. If you have ideas, suggestions, or bug fixes, you can submit pull requests or open issues directly on the game's GitHub repository.

---

### **License**
The game is licensed under the MIT License, which means it's free to use, modify, and distribute. The full details are available in the LICENSE file in the repository.

**idlegame** is a simple and engaging way to use downtime productively or just unwind. It merges basic scripting with casual gameplay, making it a fun tool for coders.
