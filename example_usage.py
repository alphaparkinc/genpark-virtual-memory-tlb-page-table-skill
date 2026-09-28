from client import VirtualMemoryTLB

def main():
    vm = VirtualMemoryTLB(tlb_size=2, page_size=4096)
    vm.map_page(0, 5)
    vm.map_page(1, 8)
    # First access: TLB miss
    m = vm.translate(100)
    # Second access: TLB hit
    h = vm.translate(200)
    print("Virtual Memory TLB Verification:")
    print(f"Access 1 (Miss): {m}")
    print(f"Access 2 (Hit): {h}")

if __name__ == "__main__":
    main()
