#!/bin/bash
import requests
from requests.exceptions import MissingSchema
from bs4 import BeautifulSoup
from requests.sessions import InvalidSchema

__copyright__="Copyright 2021 Codex-Major"
__license__="MIT"

logfile='./internet_map.txt'
#entry_link="https://twitter.com/"
entry_link="https://www.google.com/search?q=raspberry+pi+robot&rlz=1C1VDKB_enUS976US976&sxsrf=AOaemvLwnsn9ESFvt6g1c9KeTYGUnU-Fzw:1637055916409&source=lnms&tbm=shop&sa=X&ved=2ahUKEwjavP_CzJz0AhXN454KHW_xACAQ_AUoAXoECAEQAw&biw=1920&bih=947&dpr=1#spd=10149937644586298146"

def main(links):
    try:
        #print(f'\n[!] Links:{links}\n')
        for lnk in links:
            try:
                #print(lnk)
                page=requests.get(str(lnk))
                page_status = str(page.status_code)
                #print(f'[*] Link: {lnk}')
                #print('\n'+'[*] Status: '+page_status+'\n')
                #print(type(page_status))
                if page_status == '200':
                    soup=BeautifulSoup(page.content, 'html.parser')
                    tags=soup.find_all('a')
                    for tag in tags:
                        #print('\n-----------------------------------------------------------\n')
                        #print(f'parsing tags for: {link}')
                        #print(f'tag: {str(tag)}\n')
                        taglink=tag.get('href')
                        #print(f'taglink: {taglink}')
                        try:
                            if "http://" in taglink or "https://" in taglink:
                                if "/url?q=https://" in taglink or "/url?q=http://" in taglink:
                                    #print(f"[!] Not adding {taglink}")
                                else:
                                    if not (taglink == None):
                                        cnt=0
                                        for l in links:
                                            if l==taglink:
                                                cnt=1
                                                #print(f"[!] Already have: {taglink}")
                                        if cnt==0:
                                            with open(logfile, 'r+') as f:
                                                cnt1=0
                                                for line in f:
                                                    #print(line)
                                                    if line == taglink:
                                                        cnt1=1
                                                        #print(f"[!] Already have: {taglink}")
                                                        break
                                                if cnt1==0:
                                                    #print(f'[+] Adding link: {taglink}')
                                                    links.append(taglink)
                                                    f.write(taglink+"\n")
                                    else:
                                        pass
                            else:
                                pass
                                #print(f"[!] Not adding: {taglink}")
                            #time.sleep(3)
                        except TypeError:
                            pass
                            #print("[!] There was a TypeError.")
                            #exit()
                else:
                    pass
                    #print('\n'+'[*] Status: '+page_status+'\n')
            except InvalidSchema:
                #print("INVALID SCHEMA")
                pass  
        main(links)
        
    except MissingSchema:
        #print('[!] Not a valid link. Please prepend "http://" or "https://", respectively.\n')
        exit()

if __name__ == '__main__':
    try:
        links=[entry_link]
        main(links)
    except KeyboardInterrupt:
        #print('\n[!] Ctrl+C Interrupt. Quitting!\n')
        exit(0)
