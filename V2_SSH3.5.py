import tkinter as tk
from tkinter import ttk
import paramiko
import time


class SSHApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SSH Command Sender - 192.168.1.35")
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
        self.hostname = "192.168.1.35"
        self.username = "root"
        self.password = "M0d3rn@!@#24"

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):

        # Connection Frame
        self.connection_frame = tk.Frame(self.root, bg="#e6f2ff")
        self.connection_frame.pack(pady=10)

        self.connect_button = tk.Button(self.connection_frame, text="Connect", command=self.connect_ssh, width=20,
                                        bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        self.connect_button.grid(row=0, column=0, padx=10)

        self.disconnect_button = tk.Button(self.connection_frame, text="Disconnect", command=self.disconnect_ssh,
                                           width=20, bg="#f44336", fg="white", font=("Arial", 12, "bold"))
        self.disconnect_button.grid(row=0, column=1, padx=10)

        # Command Selection Frame
        self.command_frame = tk.LabelFrame(self.root, text="Command Settings", bg="#e6f2ff", font=("Arial", 12, "bold"),
                                           labelanchor="n")
        self.command_frame.pack(pady=10, padx=20, fill="x", expand=True)

        # Rate Selection
        self.rate_label = tk.Label(self.command_frame, text="Rate: \n 12M=a \n 128=n \n 144=ac", font=("Arial", 12), bg="#e6f2ff")
        self.rate_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.rate_combobox = ttk.Combobox(self.command_frame, values=["12", "128", "144"], width=18,
                                          font=("Arial", 12))
        self.rate_combobox.grid(row=0, column=1, padx=5, pady=5)


        # Channel Selection
        self.channel_label = tk.Label(self.command_frame, text="Channel:", font=("Arial", 12), bg="#e6f2ff")
        self.channel_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.channel_combobox = ttk.Combobox(self.command_frame, values=["36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "83", "84", "85", "86", "87", "88", "89", "90", "91", "92", "93", "94", "95", "96", "97", "98", "99", "100", "101", "102", "103", "104", "105", "106", "107", "108", "109", "110", "111", "112", "113", "114", "115", "116", "117", "118", "119", "120", "121", "122", "123", "124", "125", "126", "127", "128", "129", "130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "140", "141", "142", "143", "144", "145", "146", "147", "148", "149", "150", "151", "152", "153", "154", "155", "156", "157", "158", "159", "160", "161"
], width=18,
                                             font=("Arial", 12))
        self.channel_combobox.grid(row=1, column=1, padx=5, pady=5)

        # Bandwidth Selection
        self.bandwidth_label = tk.Label(self.command_frame, text="Bandwidth: \n 0=20M \n 1=40M \n 2=80M", font=("Arial", 12), bg="#e6f2ff")
        self.bandwidth_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        """self.bandwidth_combobox = ttk.Combobox(self.command_frame, values=["20M", "40M", "80M"], width=18,
                                               font=("Arial", 12))"""
        self.bandwidth_combobox = ttk.Combobox(self.command_frame, values=["0", "1", "2"], width=18,
                                               font=("Arial", 12))
        self.bandwidth_combobox.grid(row=2, column=1, padx=5, pady=5)

        # Antenna Selection
        self.antenna_label = tk.Label(self.command_frame, text="Antenna:", font=("Arial", 12), bg="#e6f2ff")
        self.antenna_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.antenna_combobox = ttk.Combobox(self.command_frame, values=["a", "b"], width=18, font=("Arial", 12))
        self.antenna_combobox.grid(row=3, column=1, padx=5, pady=5)

        '''# Power Selection
        self.power_label = tk.Label(self.command_frame, text="Power:", font=("Arial", 12), bg="#e6f2ff")
        self.power_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.power_combobox = ttk.Combobox(self.command_frame, values=["0", "11", "6"], width=18,
                                           font=("Arial", 12))
        self.power_combobox.grid(row=4, column=1, padx=5, pady=5)'''

        # Start and Stop buttons
        self.start_button = tk.Button(self.command_frame, text="Start", command=self.start_tx, width=20, bg="#4CAF50",
                                      fg="white", font=("Arial", 12, "bold"))
        self.start_button.grid(row=5, column=0, pady=10, padx=5)

        self.stop_button = tk.Button(self.command_frame, text="Stop", command=self.stop_tx, width=20, bg="#f44336",
                                     fg="white", font=("Arial", 12, "bold"))
        self.stop_button.grid(row=5, column=1, pady=10, padx=5)

        # Status Display
        self.status_label = tk.Label(self.root, text="Status: Not connected", font=("Arial", 12), bg="#e6f2ff")
        self.status_label.pack(pady=10)

    def update_status(self, status):
        self.status_label.config(text=f"Status: {status}")

    def connect_ssh(self):
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(self.hostname, username=self.username, password=self.password, timeout=10)
            self.channel = self.ssh_client.invoke_shell()
            self.update_status("Connected")
            time.sleep(5)  # Delay to ensure the channel is ready
            # Initial commands
            self.channel.send('debug\n')
            print("debug")
            time.sleep(5)
            self.channel.send(
                '33j2GiBvhpbbeunfw28NlrZIqJNsDy/JYPSIKIu6SdDVRPcT3J4gGkPXte53XVkRW92uJEGL8P83flekBNnmjzoFXKs2D8YcDoC2XcKbHLduL1Z6kjbYIzqfnJzjZ9ZMIaNF0y3dG4+UXJtmyI3zmPFEpOcjD/j4TQiQCwFGvko=\n')
            print("Chave enviada")
        except paramiko.AuthenticationException:
            self.update_status("Authentication failed, please check your username and password.")
        except paramiko.SSHException as e:
            self.update_status(f"Failed to establish SSH connection: {e}")
        except Exception as e:
            self.update_status(f"Failed to connect: {e}")

    def execute_command(self, command):
        if self.channel:
            self.channel.send(command + '\n')
            time.sleep(1)  # Adjust delay as necessary

    def start_tx(self):
        if not self.channel:
            self.update_status("Not connected to SSH")
            return


        rate = self.rate_combobox.get()
        channel = self.channel_combobox.get()
        bandwidth = self.bandwidth_combobox.get()
        antenna = self.antenna_combobox.get()
        #power = self.power_combobox.get()

        if channel and bandwidth and antenna:
            self.execute_command(f"iwpriv wlan1 mp_start")
            self.execute_command(f"iwpriv wlan1 mp_rate {rate}")
            self.execute_command(f"iwpriv wlan1 mp_channel {channel}")
            self.execute_command(f"iwpriv wlan1 mp_bandwidth 40M={bandwidth},shortGI=0")
            self.execute_command(f"iwpriv wlan1 mp_ant_tx {antenna}")
            #self.execute_command(f"iwpriv wlan1 mp_txpower patha={power}")
            self.execute_command(f"iwpriv wlan1 mp_ctx background,pkt")
            self.update_status("Transmission started.")
            print("Rate:", rate, "Channel:", channel, "\n", "BW:", bandwidth, "\n", "Ant:", antenna) #, "\n", "TxPower:",power)
        else:
            self.update_status("Please complete all selections.")

    def stop_tx(self):
        if self.channel:
            self.execute_command("iwpriv wlan1 mp_stop")
            self.update_status("Transmission stopped.")
            print("Stop")
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
