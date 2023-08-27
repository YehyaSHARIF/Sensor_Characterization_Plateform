#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 11:18:52 2023

@author: yehya
"""

# from pynput import keyboard
# # This function is called when a key is pressed. It checks if the pressed key matches the target key.
# def on_key_press(key, target_key):
#     if key == target_key:
#         return False  # Stop listening

# # This function waits for a specific key to be pressed.
# def wait_for_key(target_key_str):
#     # Convert the target key string to a KeyCode object.
#     target_key = keyboard.KeyCode.from_char(target_key_str)
    
#     # Set up a keyboard listener that will call the on_key_press function when a key is pressed.
#     with keyboard.Listener(on_press=lambda key: on_key_press(key, target_key)) as listener:
#         # Start listening for key presses and wait until the target key is pressed.
#         listener.join()

# print("Press H Key :")
# wait_for_key('h')
# print("Hello Paul")

value = input("Press Enter:\n")
 
print(f'You just pressed enter key')