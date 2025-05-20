import random
import argparse
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate

class Colors:
    RESET   = '\033[0m'
    BLACK   = '\033[30m'
    RED     = '\033[31m'
    GREEN   = '\033[32m'
    YELLOW  = '\033[33m'
    BLUE    = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN    = '\033[36m'
    WHITE   = '\033[37m'
    GRAY    = '\033[90m'
    ORANGE  = '\033[91m'
    PURPLE = '\033[1;95m' # bold purple 
    BRIGHT_RED     = '\033[91m'
    BRIGHT_GREEN   = '\033[92m'
    BRIGHT_YELLOW  = '\033[93m'
    BRIGHT_BLUE    = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN    = '\033[96m'
    BRIGHT_WHITE   = '\033[97m'

class CacheSim:
    def __init__(self, csize, bsize, assoc, replace_rule, show_stats=True):
        """
        My cache simulator that I made
        """
        self.csize = csize
        self.bsize = bsize
        self.assoc = assoc
        self.replace_rule = replace_rule.upper()
        self.num_blocks = csize // bsize
        
        # full assoc
        if assoc == -1:
            self.num_sets = 1
            self.set_size = self.num_blocks
        else:
            self.set_size = assoc
            self.num_sets = self.num_blocks // self.set_size
        
        self.cache = [[] for _ in range(self.num_sets)]
        
        self.hits = 0
        self.misses = 0
        self.accesses = 0

        # for LRU and FIFO
        self.time = 0
        
        self.good_addresses = []
        self.bad_addresses = []
        self.all_addresses = []

        if show_stats:
            s = f"{Colors.GREEN}[{Colors.WHITE}+{Colors.GREEN}] {Colors.CYAN}"
            print(f"{Colors.BRIGHT_BLUE}-~-~-~-~- {Colors.YELLOW}Cache Simulator{Colors.BRIGHT_BLUE} -~-~-~-~-")
            print(f"{s}Cache Size: {Colors.WHITE}{csize}{Colors.RESET} bytes")
            print(f"{s}Block Size: {Colors.WHITE}{bsize}{Colors.RESET} bytes")
            if assoc == 1:
                print(f"{s}Type: {Colors.WHITE}Direct-Mapped")
            elif assoc == -1:
                print(f"{s}Type: {Colors.WHITE}Fully Associativ")
            else:
                print(f"{s}Type: {Colors.WHITE}{assoc}-Way Set Associativ")
            print(f"{s}Replacement Rule: {Colors.WHITE}{replace_rule}")
            print(f"{s}Number of Sets: {Colors.WHITE}{self.num_sets}")
            print(f"{s}Number of Blocks: {Colors.WHITE}{self.num_blocks}{Colors.RESET}")

    def _get_set_idx(self, addr):
        """Figure out which set the adress goes in"""

        block_num = addr // self.bsize
        
        # full assoc
        if self.assoc == -1:
            return 0
        else:
            # get set idx bits
            return block_num % self.num_sets
    
    def _get_tag(self, addr):
        """Figure out the tag for adress"""

        block_num = addr // self.bsize
        
        # full assoc
        if self.assoc == -1:
            return block_num
        else:
            # get tag bits
            return block_num // self.num_sets
    
    def check_address(self, addr):
        """
        Check if the adress is in cache or not
        """
        self.accesses += 1
        self.time += 1
        self.all_addresses.append(addr)
        
        tag = self._get_tag(addr)
        set_idx = self._get_set_idx(addr)
        cache_set = self.cache[set_idx]
        
        # Check if we have a hit
        for i, (block_tag, extra_info) in enumerate(cache_set):
            if block_tag == tag:
                # HIT : Update based on rules
                if self.replace_rule == 'LRU':
                    cache_set[i] = (tag, self.time)
                elif self.replace_rule == 'LFU':
                    cache_set[i] = (tag, extra_info + 1)
                # For FIFO we do not change anything
                
                self.hits += 1
                self.good_addresses.append(addr)
                return True
        
        # we have a miss
        self.misses += 1
        self.bad_addresses.append(addr)
        
        if self.replace_rule == 'LRU':
            extra_info = self.time
        elif self.replace_rule == 'FIFO':
            extra_info = self.time
        elif self.replace_rule == 'LFU':
            extra_info = 1
        else:  # RANDOM
            extra_info = None
        
        # If set is not full, add the block
        if len(cache_set) < self.set_size:
            cache_set.append((tag, extra_info))
        else:
            # Need to replace some block, based on rules!
            if self.replace_rule == 'LRU':
                # replace oldest used
                oldest_idx = 0
                oldest_time = cache_set[0][1]
                for i in range(len(cache_set)):
                    if cache_set[i][1] < oldest_time:
                        oldest_time = cache_set[i][1]
                        oldest_idx = i
                cache_set[oldest_idx] = (tag, extra_info)
            elif self.replace_rule == 'FIFO':
                # replae first one that came in
                oldest_idx = 0
                oldest_time = cache_set[0][1]
                for i in range(len(cache_set)):
                    if cache_set[i][1] < oldest_time:
                        oldest_time = cache_set[i][1]
                        oldest_idx = i
                cache_set[oldest_idx] = (tag, extra_info)
            elif self.replace_rule == 'LFU':
                # replace least used one
                least_used_idx = 0
                least_used_count = cache_set[0][1]
                for i in range(len(cache_set)):
                    if cache_set[i][1] < least_used_count:
                        least_used_count = cache_set[i][1]
                        least_used_idx = i
                cache_set[least_used_idx] = (tag, extra_info)
            else:
                # replace random one
                random_idx = random.randint(0, len(cache_set) - 1)
                cache_set[random_idx] = (tag, extra_info)
        
        return False
    
    def get_hit_rate(self):
        """return how many hits we have"""
        if self.accesses == 0:
            return 0
        return self.hits / self.accesses
    
    def get_miss_rate(self):
        """return how many misses we have"""
        if self.accesses == 0:
            return 0
        return self.misses / self.accesses
    
    def start_over(self):
        """erase everything to start again"""
        self.hits = 0
        self.misses = 0
        self.accesses = 0
        self.time = 0
        self.good_addresses = []
        self.bad_addresses = []
        self.all_addresses = []
        
        # make empty cache again
        self.cache = [[] for _ in range(self.num_sets)]
    
    def show_results(self):
        """showing the results"""
        s = f"{Colors.GREEN}[{Colors.WHITE}%{Colors.GREEN}] {Colors.CYAN}"
        print()
        # print(f"{Colors.BRIGHT_BLUE}-~-~-~-~-~-~- {Colors.YELLOW}Results{Colors.BRIGHT_BLUE} -~-~-~-~-~-~-")
        print(f"{Colors.BRIGHT_BLUE}************* {Colors.YELLOW}Results{Colors.BRIGHT_BLUE} *************")

        print(f"{s}Total Memory Lookups: {Colors.WHITE}{self.accesses}")
        print(f"{s}Hits: {Colors.WHITE}{self.hits}")
        print(f"{s}Misses: {Colors.WHITE}{self.misses}")
        print(f"{s}Hit Rate: {Colors.WHITE}{self.get_hit_rate():.4f}")
        print(f"{s}Miss Rate: {Colors.WHITE}{self.get_miss_rate():.4f}{Colors.RESET}")

    def make_picture(self, save_to=None):
        """
        Make a picture of our memory accesses
        """
        plt.figure(figsize=(12, 6))
        
        # Show all memory lookups
        x = list(range(len(self.all_addresses)))
        plt.scatter(x, self.all_addresses, c='gray', s=10, alpha=0.3, label='All Memory Lookups')
        
        # Show hits
        if self.good_addresses:
            hit_x = []
            hit_y = []
            for i, addr in enumerate(self.all_addresses):
                if addr in self.good_addresses and self.good_addresses.count(addr) > 0:
                    hit_x.append(i)
                    hit_y.append(addr)
                    self.good_addresses.remove(addr)  # Take it out so we dont count twice
            plt.scatter(hit_x, hit_y, c='green', s=20, label='Good lookups (Hits)')
        
        # Show misses
        if self.bad_addresses:
            miss_x = []
            miss_y = []
            for i, addr in enumerate(self.all_addresses):
                if addr in self.bad_addresses and self.bad_addresses.count(addr) > 0:
                    miss_x.append(i)
                    miss_y.append(addr)
                    self.bad_addresses.remove(addr)  # Take it out so we dont count twice
            plt.scatter(miss_x, miss_y, c='red', s=20, label='Bad lookups (Misses)')
        
        plt.title('Memory Access with Cache Hits and Misses')
        plt.xlabel('Access Number')
        plt.ylabel('Memory Address')
        plt.legend()
        plt.grid(True)
        
        if save_to:
            plt.savefig(save_to)
        else:
            plt.show()


def make_memory_accesses(pattern, how_many, max_addr):
    """
    Make a list of memory accesses with diffrent patterns
    """
    addrs = []
    
    if pattern == 'sequential':
        for i in range(how_many):
            addrs.append(i % max_addr)
    
    elif pattern == 'random':
        for _ in range(how_many):
            addrs.append(random.randint(0, max_addr - 1))
    
    elif pattern == 'loop':
        # Go through a small section over and over
        loop_size = min(100, max_addr)
        loop_start = random.randint(0, max_addr - loop_size)
        loop_addrs = list(range(loop_start, loop_start + loop_size))
        
        for i in range(how_many):
            idx = i % loop_size
            addrs.append(loop_addrs[idx])
    
    elif pattern == 'locality':
        # Stay in one area mostly but sometimes jump
        hot_size = int(0.2 * max_addr)
        hot_start = random.randint(0, max_addr - hot_size)
        
        for _ in range(how_many):
            if random.random() < 0.8:  # 80% chance stay in hot area
                addr = random.randint(hot_start, hot_start + hot_size - 1)
            else:
                if random.random() < 0.5 and hot_start > 0:
                    addr = random.randint(0, hot_start - 1)
                else:
                    addr = random.randint(hot_start + hot_size, max_addr - 1)
            addrs.append(addr)

    return addrs


def try_diffrent_rules(addrs, csize, bsize, assoc):
    """
    Try diffrent replacement rules and see which is best
    """
    rules = ['LRU', 'FIFO', 'LFU', 'RANDOM']
    results = {}
    
    for rule in rules:
        # print("\n\n")
        print(f"\n{Colors.PURPLE}{rule} Rule{Colors.WHITE}:{Colors.RESET}")
        simulator = CacheSim(csize, bsize, assoc, rule)
        for addr in addrs:
            simulator.check_address(addr)
        
        results[rule] = {
            'hit_rate': simulator.get_hit_rate(),
            'miss_rate': simulator.get_miss_rate(),
            'hits': simulator.hits,
            'misses': simulator.misses
        }
        
        simulator.show_results()
    
    return results


def try_diffrent_assoc(addrs, csize, bsize, rule):
    """
    Try diffrent associativities and see which is best
    """
    assocs = [1, 2, 4, 8, -1]  # -1 for fully associativ
    results = {}
    
    for assoc in assocs:
        if assoc == -1:
            assoc_name = "Fully Associative"
        elif assoc == 1:
            assoc_name = "Direct-Mapped"
        else:
            assoc_name = f"{assoc}-Way Set Associative"
            
        print(f"\n{Colors.PURPLE}Trying {assoc_name}{Colors.WHITE}:{Colors.RESET}")
        simulator = CacheSim(csize, bsize, assoc, rule)
        for addr in addrs:
            simulator.check_address(addr)
        
        results[assoc_name] = {
            'hit_rate': simulator.get_hit_rate(),
            'miss_rate': simulator.get_miss_rate(),
            'hits': simulator.hits,
            'misses': simulator.misses
        }
        
        simulator.show_results()
    
    return results


def try_diffrent_bsizes(addrs, csize, assoc, rule):
    """
    Try diffrent block sizes and see which is best
    """
    bsizes = [16, 32, 64, 128, 256]
    results = {}
    
    for bsize in bsizes:
        print(f"\n{Colors.PURPLE}Trying Block Size {bsize} bytes{Colors.WHITE}:{Colors.RESET}")
        simulator = CacheSim(csize, bsize, assoc, rule)
        for addr in addrs:
            simulator.check_address(addr)
        
        results[bsize] = {
            'hit_rate': simulator.get_hit_rate(),
            'miss_rate': simulator.get_miss_rate(),
            'hits': simulator.hits,
            'misses': simulator.misses
        }
        
        simulator.show_results()
    
    return results


def make_graph(results, title, xlabel, ylabel='Hit Rate'):
    """
    Make a graph from our results
    """
    plt.figure(figsize=(10, 6))
    
    categories = list(results.keys())
    hit_rates = [results[cat]['hit_rate'] for cat in categories]
    miss_rates = [results[cat]['miss_rate'] for cat in categories]
    
    x = np.arange(len(categories))
    width = 0.35
    
    plt.bar(x - width/2, hit_rates, width, label='Hit Rate')
    plt.bar(x + width/2, miss_rates, width, label='Miss Rate')
    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(x, categories, rotation=45 if len(str(categories[0])) > 5 else 0)
    plt.legend()
    plt.grid(True, axis='y')
    plt.tight_layout()
    
    plt.show()


def big_test():
    """Try lots of diffrent setups to see what works best"""
    csizes = [1024, 4096, 16384]  # 1KB, 4KB, 16KB
    bsizes = [32, 64, 128]
    assocs = [1, 2, 4, -1]  # 1 = direct-mapped, -1 = fully associativ
    rules = ['LRU', 'FIFO', 'LFU', 'RANDOM']
    patterns = ['sequential', 'random', 'loop', 'locality']

    # How many addresses to test
    how_many = 10000
    max_addr = 32768  # 32KB address space
    
    # Save all the results
    all_results = {}

    # Collect all the best setups
    table_data = []
    headers = ["Pattern", "Cache Size (B)", "Block Size (B)", "Type", "Rule", "Hit Rate"]

    # Make memory access patterns
    test_addresses = {}
    for pattern in patterns:
        test_addresses[pattern] = make_memory_accesses(pattern, how_many, max_addr)
    
    # Try everything
    print(f"{Colors.ORANGE}Doing BIG TEST...{Colors.RESET}")
    counter = 0
    for csize in csizes:
        all_results[csize] = {}
        for bsize in bsizes:
            all_results[csize][bsize] = {}
            for assoc in assocs:
                all_results[csize][bsize][assoc] = {}
                for rule in rules:
                    all_results[csize][bsize][assoc][rule] = {}
                    for pattern in patterns:
                        # Make simulator
                        simulator = CacheSim(csize, bsize, assoc, rule, show_stats=False)
                        s = f"{Colors.WHITE},{Colors.CYAN}"
                        print(f"{Colors.YELLOW}TOTAL TESTING {Colors.WHITE}[{Colors.CYAN}cache size={csize} {s} block size={bsize} {s} associativity={assoc} {s} replacement rule={rule} {s} pattern={pattern}{Colors.WHITE}]: {Colors.GREEN}{counter}{Colors.RESET}" , end='\r')
                        counter += 1

                        # Test it
                        for addr in test_addresses[pattern]:
                            simulator.check_address(addr)
                        
                        # Save results
                        all_results[csize][bsize][assoc][rule][pattern] = {
                            'hit_rate': simulator.get_hit_rate(),
                            'miss_rate': simulator.get_miss_rate(),
                            'hits': simulator.hits,
                            'misses': simulator.misses
                        }
    
    # Find the best setup for each pattern
    print(f"\n\n {Colors.PURPLE}Best Cache Setups for Each Pattern:{Colors.WHITE}")
    for pattern in patterns:
        best_rate = 0
        best_setup = None
        
        for csize in csizes:
            for bsize in bsizes:
                for assoc in assocs:
                    for rule in rules:
                        result = all_results[csize][bsize][assoc][rule][pattern]
                        if result['hit_rate'] > best_rate:
                            best_rate = result['hit_rate']
                            best_setup = (csize, bsize, assoc, rule)
        
        # Show best setup
        csize, bsize, assoc, rule = best_setup
        if assoc == -1:
            assoc_str = "Fully Associativ"
        elif assoc == 1:
            assoc_str = "Direct-Mapped"
        else:
            assoc_str = f"{assoc}-Way Set Associativ"
        
        table_data.append([
    pattern.capitalize(),
    csize,
    bsize,
    assoc_str,
    rule,
    f"{best_rate:.4f}"
    ])

    # Print the table
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

    return all_results, test_addresses


def main():
    parser = argparse.ArgumentParser(description='My Cache Simulater')
    parser.add_argument('--cache-size', type=int, default=8192, help='how big is cache in bytes')
    parser.add_argument('--block-size', type=int, default=64, help='how big are blocks in bytes')
    parser.add_argument('--associativity', type=int, default=2, help='associativty (1=direct, -1=full)')
    parser.add_argument('--policy', type=str, default='LRU', choices=['LRU', 'FIFO', 'LFU', 'RANDOM'], help='replacement rule')
    parser.add_argument('--num-accesses', type=int, default=10000, help='how many memory thingys to do')
    parser.add_argument('--address-range', type=int, default=32768, help='how big is memory')
    parser.add_argument('--pattern', type=str, default='random', choices=['sequential', 'random', 'loop', 'locality'], help='memory access pattern')
    parser.add_argument('--mode', type=str, default='single', choices=['single', 'compare-policies', 'compare-associativities', 'compare-block-sizes', 'comprehensive'], help='what type of test to do')
    
    args = parser.parse_args()
    
    if args.mode == 'comprehensive':
        big_test()
        return
    
    # Make memory accesses
    addrs = make_memory_accesses(args.pattern, args.num_accesses, args.address_range)
    
    if args.mode == 'single':
        # Do one test
        simulator = CacheSim(
            args.cache_size,
            args.block_size,
            args.associativity,
            args.policy
        )
        
        for addr in addrs:
            simulator.check_address(addr)
        
        simulator.show_results()
        simulator.make_picture()
    
    elif args.mode == 'compare-policies':
        # Try diffrent rules
        results = try_diffrent_rules(addrs, args.cache_size, args.block_size, args.associativity)
        make_graph(results, 'Comparing Diffrent Rules', 'Replacement Rule')
    
    elif args.mode == 'compare-associativities':
        # Try diffrent associativties
        results = try_diffrent_assoc(addrs, args.cache_size, args.block_size, args.policy)
        make_graph(results, 'Comparing Diffrent Associativities', 'Associativty')
    
    elif args.mode == 'compare-block-sizes':
        # Try diffrent block sizes
        results = try_diffrent_bsizes(addrs, args.cache_size, args.associativity, args.policy)
        make_graph(results, 'Comparing Diffrent Block Sizes', 'Block Size (bytes)')


if __name__ == '__main__':
    main()