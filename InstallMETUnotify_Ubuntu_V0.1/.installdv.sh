#!/bin/bash

# COPY PROGRAM FILES
sudo cp -a ./.METUnotify ~/
sudo cp -a ./.METUnotify/METUnotifyIcons /usr/share/icons/
cp ./.METUnotify/METUnotify.desktop ~/Desktop
clear
# USERNAME - PASSWORD
echo "Your username and password will be encrypted."
echo "Type your username, press enter."
echo "Type your password, press enter."
echo "After writing as shown, please press CTRL+D"
echo ""
echo "e123456"
echo "thisIsMyPassword"
echo ""
# Python ile sifreleme algoritmasi buraya eklenecek. Hazirlaniyor...
cat > ~/.METUnotify/.uspw
clear
# SUCCESSFULLY FINISH
echo "_______________________________________"
echo "|                                     |"
echo "| #     #   ####  #######  #   #      |"
echo "| ##   ##   #        #     #   #      |"
echo "| # # # #   ###      #     #   #  NCC |"
echo "| #  #  #   #        #     #   #      |"
echo "| #     #   ####     #     #####      |"
echo "|_____________________________________|"
echo "METUnotify is successfully installed."
echo "Icon copied to Desktop."
echo "Thanks for using METUnotify."
echo "Developer     : -----Furkan TOKAC-----"
echo "Icon Designer : ----Alper EYUPOGLU----"
echo "-------------Enjoy :)-----------------"
echo ""
