import tkinter as tk
from tkinter import ttk
import paramiko
import time

class SSHApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SSH Command Sender")
        self.root.geometry("600x500")
        self.root.config(bg="#e6f2ff")

        # Centralizar a janela
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 600
        window_height = 500
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        self.root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

        # SSH connection details
        self.ssh_client = None
        self.channel = None
        self.username = "root"
        self.password = "M0d3rn@!@#24"

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        # Connection Frame
        self.connection_frame = tk.Frame(self.root, bg="#e6f2ff")
        self.connection_frame.pack(pady=10)

        self.connect_button = tk.Button(
            self.connection_frame, text="Connect", command=self.connect_ssh, width=20,
            bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        self.connect_button.grid(row=0, column=0, padx=10, pady=5)

        self.disconnect_button = tk.Button(
            self.connection_frame, text="Disconnect", command=self.disconnect_ssh, width=20,
            bg="#f44336", fg="white", font=("Arial", 12, "bold"))
        self.disconnect_button.grid(row=0, column=1, padx=10, pady=5)

        # Command Selection Frame
        self.command_frame = tk.LabelFrame(
            self.root, text="Command Settings", bg="#e6f2ff", font=("Arial", 12, "bold"),
            labelanchor="n", borderwidth=2, relief="groove")
        self.command_frame.pack(pady=10, padx=20, fill="x", expand=True)

        # IP Selection
        self.ip_label = tk.Label(self.command_frame, text="Selecione o IP:",
                                 font=("Arial", 12), bg="#e6f2ff")
        self.ip_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        self.ip_combobox = ttk.Combobox(
            self.command_frame, values=["192.168.1.35", "192.168.1.36"],
            width=18, font=("Arial", 12))
        self.ip_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Channel Selection
        self.channel_label = tk.Label(self.command_frame, text="Channel:",
                                      font=("Arial", 12), bg="#e6f2ff")
        self.channel_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.channel_combobox = ttk.Combobox(
            self.command_frame, values=[str(i) for i in range(36, 162)], width=18,
            font=("Arial", 12))
        self.channel_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Bandwidth Selection
        self.bandwidth_label = tk.Label(self.command_frame, text="Bandwidth: \n 0=20M \n 1=40M \n 2=80M",
                                        font=("Arial", 12), bg="#e6f2ff")
        self.bandwidth_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")

        self.bandwidth_combobox = ttk.Combobox(
            self.command_frame, values=["0", "1", "2"], width=18, font=("Arial", 12))
        self.bandwidth_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Antenna Selection
        self.antenna_label = tk.Label(self.command_frame, text="Antenna:", font=("Arial", 12), bg="#e6f2ff")
        self.antenna_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")

        self.antenna_combobox = ttk.Combobox(
            self.command_frame, values=["a", "b"], width=18, font=("Arial", 12))
        self.antenna_combobox.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Start and Stop Buttons
        self.start_button = tk.Button(
            self.command_frame, text="Start", command=self.start_tx, width=20,
            bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        self.start_button.grid(row=4, column=0, pady=10, padx=5)

        self.stop_button = tk.Button(
            self.command_frame, text="Stop", command=self.stop_tx, width=20,
            bg="#f44336", fg="white", font=("Arial", 12, "bold"))
        self.stop_button.grid(row=4, column=1, pady=10, padx=5)

        # Status Display
        self.status_label = tk.Label(
            self.root, text="Status: Not connected", font=("Arial", 12), bg="#e6f2ff", anchor="w")
        self.status_label.pack(fill="x", padx=20, pady=10)

    def connect_ssh(self):
        self.hostname = self.ip_combobox.get()  # Aqui a hostname é definida após a criação de ip_combobox
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(self.hostname, username=self.username, password=self.password, timeout=10)
            self.channel = self.ssh_client.invoke_shell()
            self.update_status("Connected")
            time.sleep(5)  # Delay para garantir que o canal está pronto

            # Comandos iniciais
            self.channel.send('debug\n')
            print("debug")
            time.sleep(5)
            self.channel.send(
                '33j2GiBvhpbbeunfw28NlrZIqJNsDy/JYPSIKIu6SdDVRPcT3J4gGkPXte53XVkRW92uJEGL8P83flekBNnmjzoFXKs2D8YcDoC2XcKbHLduL1Z6kjbYIzqfnJzjZ9ZMIaNF0y3dG4+UXJtmyI3zmPFEpOcjD/j4TQiQCwFGvko=\n')
            print("Chave enviada")
            # Start checking connection status
            self.root.after(1000, self.check_connection)  # Check every second
        except paramiko.AuthenticationException:
            self.update_status("Authentication failed, please check your username and password.")
        except paramiko.SSHException as e:
            self.update_status(f"Failed to establish SSH connection: {e}")
        except Exception as e:
            self.update_status(f"Failed to connect: {e}")

    def check_connection(self):
        """Check if the SSH connection is still active."""
        if self.ssh_client and not self.ssh_client.get_transport().is_active():
            self.update_status("Disconnected from SSH")
            self.ssh_client = None
            self.channel = None
        else:
            self.root.after(1000, self.check_connection)  # Keep checking every second

    def execute_command(self, command):
        if self.channel:
            self.channel.send(command + '\n')
            time.sleep(1)  # Adjust delay as necessary

    def start_tx(self):
        if not self.channel:
            self.update_status("Not connected to SSH")
            return

        channel = self.channel_combobox.get()
        bandwidth = self.bandwidth_combobox.get()
        antenna = self.antenna_combobox.get()

        if channel and bandwidth and antenna:
            self.execute_command(f"iwpriv wlan1 mp_start")
            self.execute_command(f"iwpriv wlan1 mp_channel {channel}")
            self.execute_command(f"iwpriv wlan1 mp_bandwidth 40M={bandwidth},shortGI=0")
            self.execute_command(f"iwpriv wlan1 mp_ant_tx {antenna}")
            self.execute_command(f"iwpriv wlan1 mp_ctx background,pkt")
            self.update_status("Transmission started.")
            print("Channel:", channel, "\n", "BW:", bandwidth, "\n", "Ant:", antenna)
        else:
            self.update_status("Please complete all selections.")

    def stop_tx(self):
        if self.channel:
            self.execute_command("iwpriv wlan1 mp_stop")
            self.update_status("Transmission stopped.")
        else:
            self.update_status("Not connected to SSH")

    def disconnect_ssh(self):
        if self.ssh_client:
            self.ssh_client.close()
            self.ssh_client = None
            self.channel = None
            self.update_status("Disconnected from SSH")

    def update_status(self, status):
        self.status_label.config(text=f"Status: {status}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SSHApp(root)
    root.mainloop()
