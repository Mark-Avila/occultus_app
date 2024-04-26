import customtkinter as ctk
import os
import datetime
from os import startfile
from tkinter.messagebox import askyesno
import shutil


class OutputCard(ctk.CTkFrame):
    def __init__(self, parent, title, created_date, path):
        ctk.CTkFrame.__init__(self, parent, height=72)

        info_wrapper = ctk.CTkFrame(self, fg_color="transparent")
        info_wrapper.grid(column=0, row=0, sticky="nsew")  # Set sticky to "nsew"
        self.grid_columnconfigure(0, weight=1)  # Configure column weight

        video_title = ctk.CTkLabel(
            info_wrapper,
            text=title,
            anchor="w",
            justify="left",
            font=ctk.CTkFont(weight="bold", size=12),
        )
        video_title.pack(fill="x", padx=24, pady=(12, 0))

        video_created = ctk.CTkLabel(
            info_wrapper,
            text=created_date,
            anchor="w",
            justify="left",
            font=ctk.CTkFont(size=12),
        )
        video_created.pack(fill="x", padx=24, pady=(0, 12))

        btns_wrapper = ctk.CTkFrame(self, fg_color="transparent")
        btns_wrapper.grid(column=1, row=0, sticky="nsew")  # Set sticky to "nsew"
        self.grid_columnconfigure(1, weight=1)  # Configure column weight

        video_path = self._get_videos_in_folder(path)

        view_btn = ctk.CTkButton(
            btns_wrapper,
            text="View",
            width=86,
            command=lambda: self.view_file(video_path[0]),
        )
        view_btn.pack(pady=(16, 0), padx=(156, 0))

        del_btn = ctk.CTkButton(
            btns_wrapper,
            text="Delete",
            width=86,
            command=lambda: self.delete_file(path),
        )
        del_btn.pack(pady=4, padx=(156, 0))

        copy_btn = ctk.CTkButton(btns_wrapper, text="Copy", width=86)
        copy_btn.pack(pady=(0, 16), padx=(156, 0))

    def view_file(self, path):
        print(path)
        startfile(path)

    def delete_file(self, path):
        answer = askyesno("Delete file", "Are you sure you want to delete this video?")

        if answer:
            shutil.rmtree(path)
            self.destroy()

    def _get_videos_in_folder(self, folder_path):
        videos = []
        for filename in os.listdir(folder_path):
            if filename.endswith(
                (".mp4", ".avi", ".mkv", ".mov")
            ):  # Add more video extensions if needed
                video_path = os.path.join(folder_path, filename)
                videos.append(video_path)
        return videos


class OutputPage(ctk.CTkFrame):
    def __init__(
        self, parent: ctk.CTk, controller, text="Detecting faces. Please wait"
    ):
        ctk.CTkFrame.__init__(self, parent)

        CARD_PADDING_Y = 4

        header = ctk.CTkLabel(
            self,
            text="Output History",
            anchor="w",
            justify="left",
            font=ctk.CTkFont(weight="bold", size=24),
        )
        header.pack(fill="x", padx="12", pady=18)

        container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True)

        output_dir = "output"

        folders = os.listdir(output_dir)

        for folder in folders:
            file_path = f"{output_dir}\\{folder}"
            c_time = os.path.getctime(file_path)
            c_date = datetime.datetime.fromtimestamp(c_time)
            formatted_date = c_date.strftime("%Y/%m/%d %H:%M:%S")
            # print(formatted_date)
            card = OutputCard(container, folder, formatted_date, file_path)
            card.pack(fill="x", pady=CARD_PADDING_Y)
