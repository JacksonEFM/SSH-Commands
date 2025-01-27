import tkinter as tk
from tkinter import ttk
import paramiko
import time


class SSHApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SSH Command Sender")
        self.root.geometry("600x450")
        self.root.config(bg="#f0f0f0")

        # SSH connection details
        self.ssh_client = None
        self.hostname = "192.168.1.35"
        self.username = "root"
        self.password = "M0d3rn@!@#24"

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        # Connection Frame
        self.connection_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.connection_frame.grid(row=0, column=0, pady=20, padx=20, sticky="ew")

        self.connect_button = tk.Button(self.connection_frame, text="Connect", command=self.connect_ssh, width=20,
                                        bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        self.connect_button.grid(row=0, column=0, padx=10)

        self.disconnect_button = tk.Button(self.connection_frame, text="Disconnect", command=self.disconnect_ssh,
                                           width=20, bg="#f44336", fg="white", font=("Arial", 12, "bold"))
        self.disconnect_button.grid(row=0, column=1, padx=10)

        # Command Selection Frame
        self.command_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.command_frame.grid(row=1, column=0, pady=10, padx=20, sticky="ew")

        # Rate Selection
        self.rate_label = tk.Label(self.command_frame, text="Rate:", font=("Arial", 12), bg="#f0f0f0")
        self.rate_label.grid(row=0, column=0, padx=5)
        self.rate_combobox = ttk.Combobox(self.command_frame, values=["6M", "12M", "128M"], width=18,
                                          font=("Arial", 12))
        self.rate_combobox.grid(row=0, column=1, padx=5)

        # Channel Selection
        self.channel_label = tk.Label(self.command_frame, text="Channel:", font=("Arial", 12), bg="#f0f0f0")
        self.channel_label.grid(row=1, column=0, padx=5)
        self.channel_combobox = ttk.Combobox(self.command_frame, values=["36", "38", "42"], width=18,
                                             font=("Arial", 12))
        self.channel_combobox.grid(row=1, column=1, padx=5)

        # Bandwidth Selection
        self.bandwidth_label = tk.Label(self.command_frame, text="Bandwidth:", font=("Arial", 12), bg="#f0f0f0")
        self.bandwidth_label.grid(row=2, column=0, padx=5)
        self.bandwidth_combobox = ttk.Combobox(self.command_frame, values=["20M", "40M", "80M"], width=18,
                                               font=("Arial", 12))
        self.bandwidth_combobox.grid(row=2, column=1, padx=5)

        # Antenna Selection
        self.antenna_label = tk.Label(self.command_frame, text="Antenna:", font=("Arial", 12), bg="#f0f0f0")
        self.antenna_label.grid(row=3, column=0, padx=5)
        self.antenna_combobox = ttk.Combobox(self.command_frame, values=["A", "B"], width=18, font=("Arial", 12))
        self.antenna_combobox.grid(row=3, column=1, padx=5)

        # Start and Stop buttons
        self.start_button = tk.Button(self.command_frame, text="Start", command=self.start_tx, width=20, bg="#4CAF50",
                                      fg="white", font=("Arial", 12, "bold"))
        self.start_button.grid(row=4, column=0, pady=10, padx=5)

        self.stop_button = tk.Button(self.command_frame, text="Stop", command=self.stop_tx, width=20, bg="#f44336",
                                     fg="white", font=("Arial", 12, "bold"))
        self.stop_button.grid(row=4, column=1, pady=10, padx=5)

        # Status Display
        self.status_label = tk.Label(self.root, text="Status: Not connected", font=("Arial", 12), bg="#f0f0f0")
        self.status_label.grid(row=2, column=0, pady=10, padx=20, sticky="ew")

        # Output Log
        self.output_log = tk.Text(self.root, height=10, width=60, font=("Arial", 10), bg="#f4f4f4", wrap=tk.WORD)
        self.output_log.grid(row=3, column=0, pady=20, padx=20, sticky="ew")
        self.output_log.config(state=tk.DISABLED)

    def update_status(self, status):
        self.status_label.config(text=f"Status: {status}")

    def connect_ssh(self):
        try:
            # Create SSH client and connect to the server
            print("Conectando...")
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(self.hostname, username=self.username, password=self.password,
                                    timeout=10)  # Timeout added
            self.update_status("Conectado")
            print("Conectado")
            time.sleep(5)
            # Execute the sequence of commands after connection
            self.execute_command("debug")  # Step 1: Send debug
            time.sleep(5)  # Delay added here
            self.execute_command(
                "33j2GiBvhpbbeunfw28NlrZIqJNsDy/JYPSIKIu6SdDVRPcT3J4gGkPXte53XVkRW92uJEGL8P83flekBNnmjzoFXKs2D8YcDoC2XcKbHLduL1Z6kjbYIzqfnJzjZ9ZMIaNF0y3dG4+UXJtmyI3zmPFEpOcjD/j4TQiQCwFGvko=")  # Step 2: Send Chave
        except paramiko.AuthenticationException:
            self.update_status("Authentication failed, please check your username and password.")
        except paramiko.SSHException as e:
            self.update_status(f"Failed to establish SSH connection: {e}")
        except Exception as e:
            self.update_status(f"Failed to connect: {e}")

    def execute_command(self, command):
        if self.ssh_client:
            try:
                print(f"Sending command: {command}")  # Print the command being sent
                # Execute the command and get the output
                stdin, stdout, stderr = self.ssh_client.exec_command(command)
                output = stdout.read().decode()
                error = stderr.read().decode()

                # Print the command output and error (if any)
                if output:
                    print(f"Output: {output}")
                    self.show_output(f"Output: {output}")
                if error:
                    print(f"Error: {error}")
                    self.show_output(f"Error: {error}")
            except Exception as e:
                self.update_status(f"Error executing command: {e}")
        else:
            self.update_status("SSH client is not connected.")

    def show_output(self, output):
        # Enable text widget to append new output
        self.output_log.config(state=tk.NORMAL)
        self.output_log.insert(tk.END, output + "\n")
        self.output_log.config(state=tk.DISABLED)

    def start_tx(self):
        if not self.ssh_client:
            self.update_status("Not connected to SSH")
            return

        rate = self.rate_combobox.get()
        channel = self.channel_combobox.get()
        bandwidth = self.bandwidth_combobox.get()
        antenna = self.antenna_combobox.get()

        try:
            if rate and channel and bandwidth and antenna:
                self.execute_command(f"iwpriv wlan1 mp_start")
                self.execute_command(f"iwpriv wlan1 mp_rate {rate}")
                self.execute_command(f"iwpriv wlan1 mp_channel {channel}")
                self.execute_command(f"iwpriv wlan1 mp_bandwidth {bandwidth}=0,shortGI=0")
                self.execute_command(f"iwpriv wlan1 mp_ant_tx {antenna}")
                self.execute_command(f"iwpriv wlan1 mp_ctx background,pkt")
            else:
                self.update_status("Invalid rate selected.")
        except Exception as e:
            self.update_status(f"Error during start transmission: {e}")

    def stop_tx(self):
        if self.ssh_client:
            self.execute_command("iwpriv wlan1 mp_stop")  # Stop transmission
            self.update_status("Transmission stopped.")
        else:
            self.update_status("Not connected to SSH")

    def disconnect_ssh(self):
        if self.ssh_client:
            self.ssh_client.close()
            self.update_status("Disconnected from SSH")
        else:
            self.update_status("Not connected to SSH")

# Create the Tkinter window and run the app
root = tk.Tk()
app = SSHApp(root)
root.mainloop()
