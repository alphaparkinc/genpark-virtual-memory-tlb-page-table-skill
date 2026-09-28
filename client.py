"""Virtual Memory TLB & Page Table Translation Simulator
100% Python Standard Library (collections).
"""

import collections

class VirtualMemoryTLB:
    """Address translation engine with LRU-managed TLB."""
    def __init__(self, tlb_size=4, page_size=4096):
        self.tlb_size = tlb_size
        self.page_size = page_size
        self.tlb = collections.OrderedDict()
        self.page_table = {}

    def map_page(self, vpn, pfn):
        self.page_table[vpn] = pfn

    def translate(self, virtual_address):
        vpn = virtual_address // self.page_size
        offset = virtual_address % self.page_size

        if vpn in self.tlb:
            pfn = self.tlb[vpn]
            self.tlb.move_to_end(vpn)
            hit = True
        elif vpn in self.page_table:
            pfn = self.page_table[vpn]
            if len(self.tlb) >= self.tlb_size:
                self.tlb.popitem(last=False)
            self.tlb[vpn] = pfn
            hit = False
        else:
            return {"page_fault": True, "physical_address": None, "tlb_hit": False}

        physical_address = pfn * self.page_size + offset
        return {"page_fault": False, "physical_address": physical_address, "tlb_hit": hit}
