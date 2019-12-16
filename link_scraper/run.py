import os
import sys
import time
import tkinter as tk
from tkinter import messagebox, filedialog
# scrapy packages
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from twisted.internet import reactor
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings

#Project packages
# from demo_project.spiders.link_scraper import LinkScraper
from helpers import get_urls_fm_csv

# # Set Search Words
# search_params = [ 'clubs', 'home', 'about' ]

# Main Application/GUI class

class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title('Links collector')
        # Width height
        master.geometry("500x220")
        master.resizable(False, False)
        # Create widgets/grid
        self.create_widgets()
        # Path to CSV file
        self.file_name = None

    def create_widgets(self):
        '''Create Widgets'''

        def create_left_frame():
            '''Create Left Frame with Params selector, URL processed and Proxies'''
            left_frame = tk.Frame(self.master, padx=5, pady=5)
            left_frame.grid(row=0, column=0)
            left_frame.rowconfigure(0, weight=1)
            left_frame.columnconfigure(0, weight=1)

            def add_group1():
                '''Add widget with Link params, URL process and proxies'''
                group1 = tk.LabelFrame(left_frame, text="Link parameters", padx=5, pady=5 )
                group1.grid(row=0, column=1, sticky=tk.NW)
            
                '''Fields for group-1 includes Params 1,2,3,4,5,6'''
                self.link_param1 = tk.StringVar()
                self.link_param2 = tk.StringVar()
                self.link_param3 = tk.StringVar()
                self.link_param4 = tk.StringVar()
                self.link_param5 = tk.StringVar()
                self.link_param6 = tk.StringVar()

                lp21 = tk.Label(group1, text="Param1")
                lp21.grid(row=1, column=1, sticky=(tk.W, tk.E))
                self.param1_entry = tk.Entry(group1, width=31, textvariable=self.link_param1)
                self.param1_entry.grid(row=1, column=2, sticky=(tk.W, tk.E))

                lp22 = tk.Label(group1, text="Param2")
                lp22.grid(row=2, column=1, sticky=(tk.W, tk.E))
                self.param2_entry = tk.Entry(group1, width=31, textvariable=self.link_param2)
                self.param2_entry.grid(row=2, column=2, sticky=(tk.W, tk.E))

                lp23 = tk.Label(group1, text="Param3")
                lp23.grid(row=3, column=1, sticky=(tk.W, tk.E))
                self.param3_entry = tk.Entry(group1, width=31, textvariable=self.link_param3)
                self.param3_entry.grid(row=3, column=2, sticky=(tk.W, tk.E))

                lp24 = tk.Label(group1, text="Param4")
                lp24.grid(row=4, column=1, sticky=(tk.W, tk.E))
                self.param4_entry = tk.Entry(group1, width=31, textvariable=self.link_param4)
                self.param4_entry.grid(row=4, column=2, sticky=(tk.W, tk.E)
                )
                lp25 = tk.Label(group1, text="Param5")
                lp25.grid(row=5, column=1, sticky=(tk.W, tk.E))
                self.param5_entry = tk.Entry(group1, width=31, textvariable=self.link_param5)
                self.param5_entry.grid(row=5, column=2, sticky=(tk.W, tk.E))

                lp26 = tk.Label(group1, text="Param6")
                lp26.grid(row=6, column=1, sticky=(tk.W, tk.E))
                self.param6_entry = tk.Entry(group1, width=31, textvariable=self.link_param6)
                self.param6_entry.grid(row=6, column=2, sticky=(tk.W, tk.E))
            def add_group2():
                ''' Group-2 - Urls and proxies '''
                group2 = tk.LabelFrame(left_frame,  padx=5, pady=5, border=0 )
                group2.grid(row=1, column=1, sticky=tk.NW)

                url_process = tk.Label(group2, text="URL processed / Total :")
                proxy_used = tk.StringVar()
                proxy_used = tk.Label(group2, text="Proxies:")
                url_process.grid(row=1, column=1, sticky=(tk.W))
                proxy_used.grid(row=2, column=1, sticky=(tk.W))

                proxy_used_data = tk.Label(group2, 
                textvariable=proxy_used)
                proxy_used_data.grid(row=3, column=2, sticky=tk.E)
            add_group1()
            # add_group2()

        def create_right_frame():
            '''Create Right Frame with URLs selector and Proxy anabling'''
            right_frame = tk.Frame(self.master, padx=5, pady=5)
            right_frame.grid(row=0, column=1, sticky=tk.N+tk.W+tk.E)
            right_frame.rowconfigure(0, weight=1)
            right_frame.columnconfigure(0, weight=1)

            def add_group1_2():
                '''URLs selector'''
                group1_2 = tk.LabelFrame(right_frame, text="URLs", padx=5, pady=5, width=90 )
                group1_2.grid(row=0, column=1, sticky=tk.N+tk.W+tk.E)
                group1_2.rowconfigure(0, weight=1)
                group1_2.columnconfigure(0, weight=1)

                # === Add label
                label = tk.Label(group1_2, text="You can load URLs from CSV file. \nBy default script uses 'urls.csv' file from same directory.", justify = tk.LEFT, wraplength=220)
                label.grid(row=1, column=1, sticky=(tk.W+tk.E))
                label.rowconfigure(0, weight=1)
                label.columnconfigure(0, weight=1)
                
                # == Add button
                button = tk.Button(group1_2, text = 'Load CSV with URL',command = self.load_urls_csv) 
                button.grid(row=2, column=1, sticky=tk.W+tk.E)

                # === Add success CSV Load 
                self.success_csv = tk.StringVar()
                self.success_csv.set('')
                success_csv_label = tk.Label(group1_2, textvariable=self.success_csv, fg='green')
                success_csv_label.grid(row=3, column=0, columnspan = 2, sticky=tk.W)

            def add_group2_2():
                '''Proxies selecrtor'''
                group2_2 = tk.LabelFrame(right_frame, text="URLs", padx=5, pady=5, width=90 )
                group2_2.grid(row=1, column=1, sticky=tk.NW)

                # Add label
                label = tk.Label(group2_2, text="You are able to use proxies. \nEach request it will use random proxy from list", justify = tk.LEFT)
                # label.grid(row=1, column=1, sticky=(tk.W))
                label.pack(fill = "x")
                # Add checkbox
                checkbox = tk.Checkbutton(group2_2, text="Enable Proxy")
                # checkbox.grid(row=2, column=1, sticky=tk.W)
                checkbox.pack(side = "left")
                # Add button
                button = tk.Button(group2_2, text = 'Load CSV with Proxies',command = 'self.load_urls_csv') 
                # button.grid(row=3, column=1, sticky=tk.W)
                button.pack(fill = "x")
            add_group1_2()
            # add_group2_2()

        def create_bottom_frame():
            '''Create Bottom Frame with main Button'''
            bottom_frame = tk.Frame(self.master, padx=5, pady=5)
            bottom_frame.grid(row=1, column=0, columnspan = 2, sticky=tk.N+tk.W+tk.E+tk.S)
            bottom_frame.rowconfigure(0, weight=1)
            bottom_frame.columnconfigure(0, weight=1)

            # === Add button Text var
            self.run_stop_button_text = tk.StringVar()
            self.run_stop_button_text.set('Start Scraping')
            # Add Run/Stop Button
            self.run_stop_button = tk.Button(bottom_frame,
                                textvariable=self.run_stop_button_text, 
                                command=self.run_scraper )
                                # command=self.run_scraper_Process )
            self.run_stop_button.grid(row=2, column=0, 
                        columnspan = 2, sticky=tk.W+tk.E)
            self.run_stop_button.rowconfigure(0, weight=1)
            self.run_stop_button.columnconfigure(0, weight=1)
            # run_stop_button.pack(fill = "x")

            # === Add Label
            self.success_msg = tk.StringVar()
            self.success_msg.set('')
            success_msg_label = tk.Label(bottom_frame, textvariable=self.success_msg, fg='green')
            success_msg_label.grid(row=3, column=0, columnspan = 2, sticky=tk.W)


        # Setup defaults - search words in links
        def set_default():
            ''' Set default value to param fields'''
            self.param1_entry.insert(0, 'local')
            self.param2_entry.insert(0, 'about')
            self.param3_entry.insert(0, 'clubs')
            self.param1_entry.focus()

        create_left_frame()
        create_right_frame()
        create_bottom_frame()
        set_default()

    def load_urls_csv(self):
        curr_dir = os.getcwd()
        ftypes = [('CSV files', '*.csv'), ('All files', '*')]
        self.file_name = filedialog.askopenfilename(initialdir = curr_dir,title = "Select csv file",filetypes =ftypes )
        if  not (self.file_name == None or self.file_name == ''):
            self.success_csv.set("CSV File loaded")
            print(self.file_name)

    # Run scraper function
    def run_scraper_Process(self):
        if self.run_stop_button.cget('text') == "Exit":
            # self.master.destroy()
            sys.exit()
            self.master.quit()

        search_words = [    self.link_param1.get(), 
                            self.link_param2.get(),
                            self.link_param3.get(),
                            self.link_param4.get(),
                            self.link_param5.get(),
                            self.link_param6.get() ]
        url_list = ["http://www.gohammond.com/category/hpl/",
                    "http://www.laughfactory.com/jokes/family-jokes",
                    "http://www.sandyspringsga.gov/residents/resident-guide/your-city/library",
                    "http://maldenpubliclibrary.org/browse-mpl/"]
        crawler = CrawlerProcess(get_project_settings())
        crawler.crawl('LinkScraper', url_list, search_words)
        crawler.start() # the script will block here
        
        print("Done")
        self.run_stop_button_text.set("Exit")
        self.success_msg.set('COMPLETE')

    # Run scraper function
    def run_scraper(self):
        if self.run_stop_button.cget('text') == "Exit":
            sys.exit()

        # Get csv file
        if  not (self.file_name == None or self.file_name == ''):            
            url_list = get_urls_fm_csv(self.file_name)
        else: # Get default csv file
            url_list = get_urls_fm_csv()
        # url_list = ["http://www.gohammond.com/category/hpl/",
                    # "http://www.laughfactory.com/jokes/family-jokes",
                    # "http://www.sandyspringsga.gov/residents/resident-guide/your-city/library",
                    # "http://maldenpubliclibrary.org/browse-mpl/"]

        if url_list is None:
            print("Not found any scv file")
            return messagebox.showwarning("WARNING", "Not found any scv file")

        search_words = [    self.link_param1.get(), 
                            self.link_param2.get(),
                            self.link_param3.get(),
                            self.link_param4.get(),
                            self.link_param5.get(),
                            self.link_param6.get() ]
        
        def run_spyder():
            runner = CrawlerRunner(get_project_settings())
            runner.crawl('LinkScraper', url_list, search_words)
            # runner.crawl('quotes') # test spider
            d = runner.join()
            d.addBoth(lambda _: reactor.stop())
            reactor.run()
        run_spyder()
        
        print("DONE")
        self.run_stop_button_text.set("Exit")
        self.success_msg.set('COMPLETE') 
    


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()