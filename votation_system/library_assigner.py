class LibraryAssigner:
    def __init__(self, library_man_tool, estremi):
        all_barcodes = library_man_tool.data[:, 0]
        # estremi = ["bar_start1", "bar_start2",...]
        self.estremi = estremi
        current_scaffale = None
        self.barcode_2_scaffale_dict = {}
        for bar in all_barcodes:
            if bar[0] in estremi:
                current_scaffale = bar
            self.barcode_2_scaffale_dict[bar[0]] = current_scaffale

    def count_libraries_matches(self, barcodes):
        scaffali_conteggio = {i : 0 for i in self.estremi}
        for bar in barcodes:
            scaff = self.barcode_2_scaffale_dict[bar]
            scaffali_conteggio[scaff[0]] += 1
        return scaffali_conteggio








