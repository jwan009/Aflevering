import tkinter as tk
import psutil
import platform
import GPUtil
from tabulate import tabulate
from datetime import datetime
from tkinter import ttk
from ipaddress import IPv4Address
from ipaddress import IPv4Network
from tkinter import *

# en metode, der gør at den omregner til værdier, der er forståeligt som "Kilobytes", "Megabytes", "Gigabyte" osv..
def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor
# ---------------------------------------------------------------
# Her opretter jeg et vindue af vores første tkinter
menu = Tk()
menu.title("Menuen")
label1 = Label(menu, text="============================").pack()
label3 = Label(menu, text="Velkommen til HARDWARE/NETVÆRKS-TOOL").pack()
label4 = Label(menu, text="============================").pack()

menu.geometry("700x700") # definer hvor stor vinduet skal være
# ---------------------------------------------------------------
# Dens funktion bl.a. er at vise CPU-, OS-, Disk-Info osv..(jeg har oprettet en metode, som kan styre analysering af hardware og software)
def hardwareanalyseren():
    top7 = Toplevel() # den åbner et nyt vindue med alle mulighederne
    top7.geometry("700x700")
    top7.title("Hardware-Analyseren")
    label = Label(top7, text="____________________________________")
    label2 = Label(top7, text="Velkommen til Hardware-Analyseren")
    label2.pack()
    label.pack()

    def den_anden_fane():
# Info om OS og Systemet
        top = Toplevel()
        my_text = Text(top, width=90, height=30) # Definering af Tekstboksen, hvor alt information kan blive udskrevet
        my_text.pack(pady=20)
        uname = platform.uname()
        my_text.insert(END, (
            f"System: {uname.system} {uname.release}"
            f"\n\nEnhedensNavn: {uname.node}"
            f"\nVersion: {uname.version}"
            f"\nMachine: {uname.machine}"
            f"\nProcessor: {uname.processor}")) # her indsætter jeg hvad der skal blive skrevet inde i tekstboksen

    def den_anden_fane2():
        # CPU Information
        top2 = Toplevel()
        my_text2 = Text(top2, width=90, height=30)
        my_text2.pack(pady=20)
        cpufreq = psutil.cpu_freq()
        my_text2.insert(END, (f"Fysiske kerner: {psutil.cpu_count(logical=False)}"
                              f"\nKerner i alt: {psutil.cpu_count(logical=True)}"
                              f"\n=================================================="
                              f"\nMax Frekvenser: {cpufreq.max:.2f}Mhz"
                              f"\nMin Frekvenser: {cpufreq.min:.2f}Mhz"
                              f"\nNuvaerende Frekvens: {cpufreq.current:.2f}Mhz"
                              f"\n=================================================="))
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            my_text2.insert(END, (f"\nCore {i}: {percentage}%"))
        my_text2.insert(END, (f"\nTotal CPU Usage: {psutil.cpu_percent()}%"))
# --------------------------------------------------------------------------------------
    def den_anden_fane3():
        # RAM Information:
        top3 = Toplevel()
        my_text3 = Text(top3, width=90, height=30)
        my_text3.pack(pady=20)
        svmem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        my_text3.insert(END, (f"RAM I alt: {get_size(svmem.total)}"
                              f"\nLedig-Plads: {get_size(svmem.available)}"
                              f"\nAnvendt-PLads: {get_size(svmem.used)}"
                              f"\nAnvendt-RAM i Procent: {svmem.percent}%"
                              f"\n\n=============== SWAP =================="
                              f"\nSWAP-RAM i alt: {get_size(swap.total)}"
                              f"\nLedig-Plads: {get_size(swap.free)}"
                              f"\nAnvendt-Plads{get_size(swap.used)}"
                              f"\nAnvendt-RAM i Procent: {swap.percent}%"))
# -----------------------------------------------------------------------------------------
    def den_anden_fane4():
        # Disk Information:
        top4 = Toplevel()
        my_text4 = Text(top4, width=90, height=30)
        my_text4.pack(pady=20)
        partitioner = psutil.disk_partitions()
        for partition in partitioner:
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:

                continue
            my_text4.insert(END, (f"\n\n=== Device: {partition.device} ==="
                                  f"\nMountpoint: {partition.mountpoint}"
                                  f"\nFile System Type: {partition.fstype}"
                                  f"\nPlads i alt: {get_size(partition_usage.total)}"
                                  f"\nAnvendt-Plads: {get_size(partition_usage.used)}"
                                  f"\nLedig-Plads: {get_size(partition_usage.free)}"
                                  f"\nAnvendt-Plads i Procent: {partition_usage.percent}"))
# -------------------------------------------------------------------------------------------
    def den_anden_fane5():
        # Netvaerks Information:
        top5 = Toplevel()
        my_text5 = Text(top5, width=150, height=70)
        my_text5.pack(pady=20)
        if_addrs = psutil.net_if_addrs()
        for interface_name, interface_addresses in if_addrs.items():
            for address in interface_addresses:
                my_text5.insert(END, (f"\n\n=== Interface: {interface_name}==="))
                if str(address.family) == 'AddressFamily.AF_INET':
                    print()
                    my_text5.insert(END, (f"\nIP-Address: {address.address}"
                                          f"\nSubnet-Mask: {address.netmask}"
                                          f"\nBroadcast IP: {address.broadcast}"
                                          f"\n======================================"))
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    my_text5.insert(END, f"\nMAC-Address: {address.address}"
                                         f"\nSubnet-Mask: {address.netmask}"
                                         f"\nBroadcast MAC: {address.broadcast}")
        net_io = psutil.net_io_counters()
        my_text5.insert(END, (f"\n\n\nAntal Data Bliver Sendt: {get_size(net_io.bytes_sent)}"
                              f"\nAntal Data Bliver Modtaget: {get_size(net_io.bytes_recv)}"))
# ----------------------------------------------------------------------------------------
    def den_anden_fane6():
        # GPU Information:
        top6 = Toplevel()
        my_text6 = Text(top6, width=110, height=40)
        my_text6.pack(pady=20)
        gpus = GPUtil.getGPUs()
        list_gpus = []
        for gpu in gpus:
            gpu_id = gpu.id
            gpu_name = gpu.name
            gpu_load = f"{gpu.load * 100}%"
            gpu_free_memory = f"{gpu.memoryFree}MB"
            gpu_used_memory = f"{gpu.memoryUsed}MB"
            gpu_total_memory = f"{gpu.memoryTotal}MB"
            gpu_temperature = f"{gpu.temperature} °C"

            my_text6.insert(END, (f"{gpu_id}"
                                  f"{gpu_name}"
                                  f"{gpu_load}%"
                                  f"\n{gpu_free_memory}MB"
                                  f"\n{gpu_used_memory}MB"
                                  f"\n{gpu_total_memory}MB"
                                  f"\n{gpu_temperature} °C"))
            gpu_uuid = gpu.uuid
            my_text6.insert(list_gpus.append((
                gpu_id, gpu_name, gpu_load, gpu_free_memory, gpu_used_memory, gpu_total_memory, gpu_temperature,
                gpu_uuid
            )))
# -----------------------------------------------------------------------------------------------------------------
# jeg har oprettet de her knapper, så man kan tilgå hver mulighed inde på Hardware-Analyseren:
    knap1OS = Button(top7, text="INFORMATION OM SYSTEMET", padx=50, borderwidth=20, command=den_anden_fane)
    knap1OS.pack()
    knap1OS.place(x=197, y=70)

    knap2CPU = Button(top7, text="CPU", padx=119, borderwidth=20, command=den_anden_fane2)
    knap2CPU.pack()
    knap2CPU.place(x=197, y=160)

    knap3RAM = Button(top7, text="RAM Information", padx=84, borderwidth=20, command=den_anden_fane3)
    knap3RAM.pack()
    knap3RAM.place(x=197, y=250)

    knap4disk = Button(top7, text="DISK Information", padx=85, borderwidth=20, command=den_anden_fane4)
    knap4disk.pack()
    knap4disk.place(x=197, y=340)

    knap5netvaerk = Button(top7, text="Netværks Information", padx=72, borderwidth=20, command=den_anden_fane5)
    knap5netvaerk.pack()
    knap5netvaerk.place(x=197, y=450)

    knap6GPU = Button(top7, text="GPU Information", padx=85, borderwidth=20, command=den_anden_fane6)
    knap6GPU.pack()
    knap6GPU.place(x=197, y=550)

# -------------------------------------------------------------------------------------------------------------

def Netvaerkssubnetteren():
# ny fane åbner til Netværkssubnetteren:
    top8 = Toplevel()
    top8.geometry("700x700")
    top8.title("Netværkssubnetteren")
    mintext = Text(top8, width=60, height=25)
    mintext.pack(pady=220, padx=75)

    labelstreg = Label(top8, text="=====================================").pack
    labelnetværk = Label(top8, text="Velkommen til Netværkssubnetteren")
    labelstreg = Label(top8, text="=====================================").pack

    ipaddresse = Label(top8, text="IP-Addresse : ")
    ipaddresse.pack()
    ipaddresse.place(x=120, y=80)

    svar = Label(top8, text="Svar : ")
    svar.pack()
    svar.place(x=70, y=220)
    labelnetværk.pack()
    labelnetværk.place(x=190, y=30)

    skrivip = Entry(top8, width=30)

    skrivip.pack()
    skrivip.place(x=199, y=82)

# her har jeg sat en funktion inde i en funktion. den gør at den viser hvilken type IPv4-addresse, vi taster ind.
    def netværksmetode():
        ip_address = IPv4Address(skrivip.get())
        mintext.insert(END, "Integer of IPv4 address: {ip}".format(ip=int(ip_address)))
        mintext.insert(END, "\n\npacked form of IPv4 address: {ip}".format(ip=ip_address.packed))
        mintext.insert(END, "\nIPv4 address: {ip}".format(ip=ip_address))
        mintext.insert(END, "")

    knaptilsubmit = Button(top8, text="Løs", padx=50, command=netværksmetode)
    knaptilsubmit.pack()
    knaptilsubmit.place(x=235, y=120)
# ---------------------------------------------------------------------------------------------------------
# Her giver jeg lidt info om hvad programmet kan bruges til
def ominfo():
    top9 = Toplevel()
    top9.title("OM Programmet")
    infotekst = Text(top9, width=80, height=35)
    infotekst.pack(padx=220, pady=75)
    infotekst.insert(END, "Programmet bruges til at findes det forskellige informationer omkring PC")
    infotekst.insert(END, "\n\nTak for dit besøg til vores lille fane")
# ---------------------------------------------------------------------------------------------------------

knaptilanalyseren = Button(menu, text="Hardware-Analyseren", padx=85, command=hardwareanalyseren)
knaptilanalyseren.pack()
knaptilanalyseren.place(x=197, y=80)

knaptilnetværksubnet = Button(menu, text="IP-Info", padx=85, command=Netvaerkssubnetteren, width=16)
knaptilnetværksubnet.pack()
knaptilnetværksubnet.place(x=199, y=140)

Omknap = Button(menu, text="OM", padx=45, command=ominfo, width=27)
Omknap.pack()
Omknap.place(x=200, y=200)

menu.mainloop() # uden den her, så kan mine fane jo ikke dukke up