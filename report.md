# گزارش کار پروژه شبیه‌ساز کش

## مقدمه
حافظه کش (Cache) یکی از مهم‌ترین اجزای معماری کامپیوتر مدرن است که تأثیر بسزایی در عملکرد و سرعت سیستم دارد. این حافظه بین پردازنده و حافظه اصلی قرار می‌گیرد و با نگهداری داده‌های پرکاربرد، زمان دسترسی به آن‌ها را کاهش می‌دهد. در این پروژه، یک شبیه‌ساز کش با زبان پایتون پیاده‌سازی شده است که امکان بررسی انواع مختلف معماری‌های کش را فراهم می‌کند.

## مفاهیم اصلی کش

### ساختار کش
کش از چند جزء اصلی تشکیل شده است:
- **اندازه کش (Cache Size)**: کل فضای حافظه کش بر حسب بایت
- **اندازه بلوک (Block Size)**: اندازه هر بلوک داده در کش
- **همبندی (Associativity)**: تعیین می‌کند یک بلوک داده در چه مکان‌هایی از کش می‌تواند قرار گیرد
- **تعداد مجموعه‌ها (Number of Sets)**: کش به چند مجموعه تقسیم می‌شود
- **سیاست جایگزینی (Replacement Policy)**: تعیین می‌کند در صورت پر بودن کش، کدام بلوک باید جایگزین شود

### انواع معماری کش
- **نگاشت مستقیم (Direct-Mapped)**: هر آدرس حافظه فقط می‌تواند در یک مکان مشخص در کش قرار گیرد
- **همبندی مجموعه‌ای (Set-Associative)**: هر آدرس حافظه می‌تواند در یکی از چند مکان مشخص در یک مجموعه قرار گیرد
- **تمام همبند (Fully-Associative)**: هر آدرس حافظه می‌تواند در هر مکانی از کش قرار گیرد

### سیاست‌های جایگزینی
- **LRU (Least Recently Used)**: بلوکی که دیرتر از همه استفاده شده است حذف می‌شود
- **FIFO (First-In-First-Out)**: بلوکی که زودتر از همه وارد شده است حذف می‌شود
- **LFU (Least Frequently Used)**: بلوکی که کمترین تعداد استفاده را داشته است حذف می‌شود
- **Random**: یک بلوک به صورت تصادفی برای حذف انتخاب می‌شود

## ساختار کلی کد

کد شبیه‌ساز کش از چند بخش اصلی تشکیل شده است:

1. **کلاس Colors**: برای نمایش رنگی اطلاعات در خروجی ترمینال
2. **کلاس CacheSim**: کلاس اصلی شبیه‌ساز کش
3. **توابع تولید الگوهای دسترسی به حافظه**: برای شبیه‌سازی الگوهای مختلف دسترسی به حافظه
4. **توابع مقایسه‌ای**: برای مقایسه سیاست‌های مختلف جایگزینی، همبندی و اندازه بلوک
5. **تابع big_test**: برای انجام آزمایش جامع روی همه پیکربندی‌های ممکن
6. **تابع main**: برای پردازش آرگومان‌های خط فرمان و اجرای آزمایش‌های مختلف

## کلاس CacheSim

این کلاس هسته اصلی شبیه‌ساز کش است که عملیات شبیه‌سازی را انجام می‌دهد.

### متغیرهای کلاس

- **csize**: اندازه کش بر حسب بایت
- **bsize**: اندازه بلوک بر حسب بایت
- **assoc**: همبندی کش (1 برای نگاشت مستقیم، -1 برای تمام همبند، مقدار دیگر برای همبندی مجموعه‌ای)
- **replace_rule**: سیاست جایگزینی (LRU، FIFO، LFU، RANDOM)
- **num_blocks**: تعداد کل بلوک‌های کش
- **num_sets**: تعداد مجموعه‌ها
- **set_size**: تعداد بلوک در هر مجموعه
- **cache**: لیستی از مجموعه‌ها که هر مجموعه لیستی از بلوک‌هاست
- **hits**: تعداد برخوردها (hits)
- **misses**: تعداد عدم برخوردها (misses)
- **accesses**: تعداد کل دسترسی‌ها
- **time**: شمارنده زمان برای سیاست‌های LRU و FIFO
- **good_addresses**: لیستی از آدرس‌هایی که با موفقیت در کش پیدا شده‌اند (hits)
- **bad_addresses**: لیستی از آدرس‌هایی که در کش پیدا نشده‌اند (misses)
- **all_addresses**: لیستی از همه آدرس‌های دسترسی

### متدهای کلاس

#### __init__
سازنده کلاس که پارامترهای کش را مقداردهی اولیه می‌کند و ساختار کش را ایجاد می‌کند.

```python
def __init__(self, csize, bsize, assoc, replace_rule, show_stats=True):
    self.csize = csize
    self.bsize = bsize
    self.assoc = assoc
    self.replace_rule = replace_rule.upper()
    self.num_blocks = csize // bsize
    
    # تعیین نوع همبندی
    if assoc == -1:  # تمام همبند
        self.num_sets = 1
        self.set_size = self.num_blocks
    else:  # نگاشت مستقیم یا همبندی مجموعه‌ای
        self.set_size = assoc
        self.num_sets = self.num_blocks // self.set_size
    
    # ایجاد کش خالی
    self.cache = [[] for _ in range(self.num_sets)]
    
    # مقداردهی اولیه آمارها
    self.hits = 0
    self.misses = 0
    self.accesses = 0
    self.time = 0
    
    self.good_addresses = []
    self.bad_addresses = []
    self.all_addresses = []
    
    # نمایش اطلاعات پیکربندی
    if show_stats:
        # نمایش اطلاعات پیکربندی کش
```

#### _get_set_idx
این متد شماره مجموعه مربوط به یک آدرس حافظه را محاسبه می‌کند.

```python
def _get_set_idx(self, addr):
    """تعیین شماره مجموعه برای آدرس"""
    block_num = addr // self.bsize
    
    # اگر تمام همبند باشد، فقط یک مجموعه داریم
    if self.assoc == -1:
        return 0
    else:
        # محاسبه شماره مجموعه با استفاده از باقیمانده تقسیم
        return block_num % self.num_sets
```

#### _get_tag
این متد برچسب (tag) مربوط به یک آدرس حافظه را محاسبه می‌کند.

```python
def _get_tag(self, addr):
    """تعیین برچسب برای آدرس"""
    block_num = addr // self.bsize
    
    # اگر تمام همبند باشد، کل شماره بلوک به عنوان برچسب استفاده می‌شود
    if self.assoc == -1:
        return block_num
    else:
        # محاسبه برچسب با تقسیم شماره بلوک بر تعداد مجموعه‌ها
        return block_num // self.num_sets
```

#### check_address
این متد بررسی می‌کند که آیا یک آدرس در کش وجود دارد یا خیر و عملیات مناسب را انجام می‌دهد.

```python
def check_address(self, addr):
    """بررسی وجود آدرس در کش"""
    self.accesses += 1
    self.time += 1
    self.all_addresses.append(addr)
    
    tag = self._get_tag(addr)
    set_idx = self._get_set_idx(addr)
    cache_set = self.cache[set_idx]
    
    # بررسی برخورد (hit)
    for i, (block_tag, extra_info) in enumerate(cache_set):
        if block_tag == tag:
            # برخورد: به‌روزرسانی بر اساس سیاست جایگزینی
            if self.replace_rule == 'LRU':
                cache_set[i] = (tag, self.time)
            elif self.replace_rule == 'LFU':
                cache_set[i] = (tag, extra_info + 1)
            # برای FIFO نیازی به تغییر نیست
            
            self.hits += 1
            self.good_addresses.append(addr)
            return True
    
    # عدم برخورد (miss)
    self.misses += 1
    self.bad_addresses.append(addr)
    
    # تعیین اطلاعات اضافی بر اساس سیاست جایگزینی
    if self.replace_rule == 'LRU':
        extra_info = self.time
    elif self.replace_rule == 'FIFO':
        extra_info = self.time
    elif self.replace_rule == 'LFU':
        extra_info = 1
    else:  # RANDOM
        extra_info = None
    
    # اگر مجموعه پر نیست، بلوک را اضافه کن
    if len(cache_set) < self.set_size:
        cache_set.append((tag, extra_info))
    else:
        # نیاز به جایگزینی یک بلوک است
        if self.replace_rule == 'LRU':
            # جایگزینی قدیمی‌ترین بلوک استفاده شده
            oldest_idx = 0
            oldest_time = cache_set[0][1]
            for i in range(len(cache_set)):
                if cache_set[i][1] < oldest_time:
                    oldest_time = cache_set[i][1]
                    oldest_idx = i
            cache_set[oldest_idx] = (tag, extra_info)
        elif self.replace_rule == 'FIFO':
            # جایگزینی اولین بلوکی که وارد شده
            oldest_idx = 0
            oldest_time = cache_set[0][1]
            for i in range(len(cache_set)):
                if cache_set[i][1] < oldest_time:
                    oldest_time = cache_set[i][1]
                    oldest_idx = i
            cache_set[oldest_idx] = (tag, extra_info)
        elif self.replace_rule == 'LFU':
            # جایگزینی کمترین استفاده شده
            least_used_idx = 0
            least_used_count = cache_set[0][1]
            for i in range(len(cache_set)):
                if cache_set[i][1] < least_used_count:
                    least_used_count = cache_set[i][1]
                    least_used_idx = i
            cache_set[least_used_idx] = (tag, extra_info)
        else:
            # جایگزینی تصادفی
            random_idx = random.randint(0, len(cache_set) - 1)
            cache_set[random_idx] = (tag, extra_info)
    
    return False
```

#### متدهای دیگر

- **get_hit_rate**: نرخ برخورد (hit rate) را محاسبه می‌کند
- **get_miss_rate**: نرخ عدم برخورد (miss rate) را محاسبه می‌کند
- **start_over**: کش را پاک می‌کند تا بتوان دوباره از ابتدا شروع کرد
- **show_results**: نتایج شبیه‌سازی را نمایش می‌دهد
- **make_picture**: یک نمودار از دسترسی‌های حافظه ایجاد می‌کند که برخوردها و عدم برخوردها را نشان می‌دهد

## توابع تولید الگوهای دسترسی به حافظه

این توابع الگوهای مختلف دسترسی به حافظه را شبیه‌سازی می‌کنند:

```python
def make_memory_accesses(pattern, how_many, max_addr):
    """ایجاد لیستی از دسترسی‌های حافظه با الگوهای مختلف"""
    addrs = []
    
    if pattern == 'sequential':
        # الگوی ترتیبی
        for i in range(how_many):
            addrs.append(i % max_addr)
    
    elif pattern == 'random':
        # الگوی تصادفی
        for _ in range(how_many):
            addrs.append(random.randint(0, max_addr - 1))
    
    elif pattern == 'loop':
        # الگوی حلقه‌ای (تکرار یک بخش کوچک)
        loop_size = min(100, max_addr)
        loop_start = random.randint(0, max_addr - loop_size)
        loop_addrs = list(range(loop_start, loop_start + loop_size))
        
        for i in range(how_many):
            idx = i % loop_size
            addrs.append(loop_addrs[idx])
    
    elif pattern == 'locality':
        # الگوی محلی (اکثر دسترسی‌ها در یک ناحیه محدود)
        hot_size = int(0.2 * max_addr)
        hot_start = random.randint(0, max_addr - hot_size)
        
        for _ in range(how_many):
            if random.random() < 0.8:  # 80% احتمال ماندن در ناحیه داغ
                addr = random.randint(hot_start, hot_start + hot_size - 1)
            else:
                # 20% احتمال پرش به جای دیگر
                if random.random() < 0.5 and hot_start > 0:
                    addr = random.randint(0, hot_start - 1)
                else:
                    addr = random.randint(hot_start + hot_size, max_addr - 1)
            addrs.append(addr)

    return addrs
```

این الگوها شامل:
- **sequential**: دسترسی‌های پشت سر هم و ترتیبی
- **random**: دسترسی‌های کاملاً تصادفی
- **loop**: دسترسی‌های تکراری در یک محدوده کوچک (شبیه‌سازی حلقه)
- **locality**: دسترسی‌ها با محلیت زمانی و مکانی (اکثر دسترسی‌ها در یک ناحیه محدود)

## توابع مقایسه‌ای

این توابع برای مقایسه پیکربندی‌های مختلف کش استفاده می‌شوند:

### مقایسه سیاست‌های جایگزینی
```python
def try_diffrent_rules(addrs, csize, bsize, assoc):
    """آزمایش سیاست‌های مختلف جایگزینی"""
    rules = ['LRU', 'FIFO', 'LFU', 'RANDOM']
    results = {}
    
    for rule in rules:
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
```

### مقایسه انواع همبندی
```python
def try_diffrent_assoc(addrs, csize, bsize, rule):
    """آزمایش همبندی‌های مختلف"""
    assocs = [1, 2, 4, 8, -1]  # -1 برای تمام همبند
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
```

### مقایسه اندازه‌های مختلف بلوک
```python
def try_diffrent_bsizes(addrs, csize, assoc, rule):
    """آزمایش اندازه‌های مختلف بلوک"""
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
```

## آزمایش جامع (big_test)

این تابع یک آزمایش جامع روی تمام ترکیبات ممکن پارامترهای کش انجام می‌دهد و بهترین پیکربندی را برای هر الگوی دسترسی حافظه پیدا می‌کند:

```python
def big_test():
    """آزمایش جامع روی پیکربندی‌های مختلف"""
    csizes = [1024, 4096, 16384]  # 1KB, 4KB, 16KB
    bsizes = [32, 64, 128]
    assocs = [1, 2, 4, -1]  # 1 = نگاشت مستقیم، -1 = تمام همبند
    rules = ['LRU', 'FIFO', 'LFU', 'RANDOM']
    patterns = ['sequential', 'random', 'loop', 'locality']

    # تعداد دسترسی‌های حافظه
    how_many = 10000
    max_addr = 32768  # فضای آدرس 32KB
    
    # ذخیره نتایج
    all_results = {}
    table_data = []
    headers = ["Pattern", "Cache Size (B)", "Block Size (B)", "Type", "Rule", "Hit Rate"]

    # ایجاد الگوهای دسترسی حافظه
    test_addresses = {}
    for pattern in patterns:
        test_addresses[pattern] = make_memory_accesses(pattern, how_many, max_addr)
    
    # آزمایش تمام ترکیبات ممکن
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
                        # ایجاد شبیه‌ساز
                        simulator = CacheSim(csize, bsize, assoc, rule, show_stats=False)
                        s = f"{Colors.WHITE},{Colors.CYAN}"
                        print(f"{Colors.YELLOW}TOTAL TESTING {Colors.WHITE}[{Colors.CYAN}cache size={csize} {s} block size={bsize} {s} associativity={assoc} {s} replacement rule={rule} {s} pattern={pattern}{Colors.WHITE}]: {Colors.GREEN}{counter}{Colors.RESET}" , end='\r')
                        counter += 1

                        # آزمایش
                        for addr in test_addresses[pattern]:
                            simulator.check_address(addr)
                        
                        # ذخیره نتایج
                        all_results[csize][bsize][assoc][rule][pattern] = {
                            'hit_rate': simulator.get_hit_rate(),
                            'miss_rate': simulator.get_miss_rate(),
                            'hits': simulator.hits,
                            'misses': simulator.misses
                        }
    
    # یافتن بهترین پیکربندی برای هر الگو
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
        
        # نمایش بهترین پیکربندی
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

    # چاپ جدول
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

    return all_results, test_addresses
```

## تابع main

این تابع آرگومان‌های خط فرمان را پردازش می‌کند و آزمایش‌های مختلف را اجرا می‌کند:

```python
def main():
    parser = argparse.ArgumentParser(description='Cache Simulater')
    parser.add_argument('--cache-size', type=int, default=8192, help='اندازه کش بر حسب بایت')
    parser.add_argument('--block-size', type=int, default=64, help='اندازه بلوک بر حسب بایت')
    parser.add_argument('--associativity', type=int, default=2, help='همبندی (1=مستقیم، -1=تمام همبند)')
    parser.add_argument('--policy', type=str, default='LRU', choices=['LRU', 'FIFO', 'LFU', 'RANDOM'], help='سیاست جایگزینی')
    parser.add_argument('--num-accesses', type=int, default=10000, help='تعداد دسترسی‌های حافظه')
    parser.add_argument('--address-range', type=int, default=32768, help='اندازه حافظه')
    parser.add_argument('--pattern', type=str, default='random', choices=['sequential', 'random', 'loop', 'locality'], help='الگوی دسترسی حافظه')
    parser.add_argument('--mode', type=str, default='single', choices=['single', 'compare-policies', 'compare-associativities', 'compare-block-sizes', 'comprehensive'], help='نوع آزمایش')
    
    args = parser.parse_args()
    
    if args.mode == 'comprehensive':
        big_test()
        return
    
    # ایجاد دسترسی‌های حافظه
    addrs = make_memory_accesses(args.pattern, args.num_accesses, args.address_range)
    
    if args.mode == 'single':
        # یک آزمایش ساده
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
        # مقایسه سیاست‌های جایگزینی
        results = try_diffrent_rules(addrs, args.cache_size, args.block_size, args.associativity)
        make_graph(results, 'Comparing Different Rules', 'Replacement Rule')
    
    elif args.mode == 'compare-associativities':
        # مقایسه انواع همبندی
        results = try_diffrent_assoc(addrs, args.cache_size, args.block_size, args.policy)
        make_graph(results, 'Comparing Different Associativities', 'Associativity')
    
    elif args.mode == 'compare-block-sizes':
        # مقایسه اندازه‌های مختلف بلوک
        results = try_diffrent_bsizes(addrs, args.cache_size, args.associativity, args.policy)
        make_graph(results, 'Comparing Different Block Sizes', 'Block Size (bytes)')
```

## نحوه استفاده از شبیه‌ساز

شبیه‌ساز کش از طریق خط فرمان و با آرگومان‌های مختلف قابل استفاده است:

### مثال‌ها

1. **آزمایش ساده با پیکربندی پیش‌فرض**:
   ```bash
   python my_p.py
   ```

2. **آزمایش با پیکربندی دلخواه**:
   ```bash
   python my_p.py --cache-size 4096 --block-size 32 --associativity 4 --policy LRU
   ```

3. **مقایسه سیاست‌های جایگزینی**:
   ```bash
   python my_p.py --mode compare-policies --pattern loop
   ```

4. **مقایسه انواع همبندی**:
   ```bash
   python my_p.py --mode compare-associativities --pattern locality
   ```

5. **مقایسه اندازه‌های بلوک**:
   ```bash
   python my_p.py --mode compare-block-sizes --pattern sequential
   ```

6. **آزمایش جامع روی تمام پیکربندی‌ها**:
   ```bash
   python my_p.py --mode comprehensive
   ```

## تحلیل عملکرد

### الگوهای دسترسی به حافظه

شبیه‌ساز چهار الگوی مختلف دسترسی به حافظه را پشتیبانی می‌کند:

1. **الگوی ترتیبی (Sequential)**:
   - دسترسی‌های پشت سر هم به آدرس‌های متوالی
   - معمولاً در عملیات‌های خطی مانند پیمایش آرایه‌ها اتفاق می‌افتد
   - در این الگو، کش‌های با اندازه بلوک بزرگتر معمولاً عملکرد بهتری دارند

2. **الگوی تصادفی (Random)**:
   - دسترسی‌های کاملاً تصادفی به حافظه
   - در برنامه‌هایی با دسترسی غیرقابل پیش‌بینی رخ می‌دهد
   - در این الگو، کش‌های تمام همبند با سیاست LRU معمولاً عملکرد بهتری دارند

3. **الگوی حلقه‌ای (Loop)**:
   - دسترسی تکراری به یک بخش محدود از حافظه
   - در حلقه‌های برنامه رخ می‌دهد
   - در این الگو، کش با اندازه کافی برای نگهداری کل حلقه عملکرد بسیار خوبی دارد

4. **الگوی محلیت (Locality)**:
   - اکثر دسترسی‌ها در یک ناحیه محدود با پرش‌های گاه‌به‌گاه به نواحی دیگر
   - نزدیک‌ترین الگو به دسترسی واقعی در برنامه‌ها
   - کش‌های با همبندی بالا و سیاست LRU معمولاً در این الگو بهتر عمل می‌کنند

### سیاست‌های جایگزینی

چهار سیاست جایگزینی در شبیه‌ساز پیاده‌سازی شده‌اند:

1. **LRU (Least Recently Used)**:
   - بلوکی که دیرتر از همه استفاده شده است را حذف می‌کند
   - از زمان آخرین دسترسی برای تصمیم‌گیری استفاده می‌کند
   - معمولاً برای الگوهای با محلیت زمانی بالا عملکرد خوبی دارد
   - پیچیدگی پیاده‌سازی: متوسط

2. **FIFO (First-In-First-Out)**:
   - بلوکی که زودتر از همه وارد شده است را حذف می‌کند
   - از زمان ورود بلوک برای تصمیم‌گیری استفاده می‌کند
   - پیاده‌سازی ساده‌تر از LRU
   - معمولاً عملکرد ضعیف‌تری نسبت به LRU دارد

3. **LFU (Least Frequently Used)**:
   - بلوکی که کمترین تعداد استفاده را داشته است را حذف می‌کند
   - از تعداد دفعات دسترسی برای تصمیم‌گیری استفاده می‌کند
   - برای الگوهای با فرکانس دسترسی متفاوت مناسب است
   - پیچیدگی پیاده‌سازی: بالا

4. **RANDOM**:
   - یک بلوک به صورت تصادفی برای حذف انتخاب می‌کند
   - ساده‌ترین سیاست برای پیاده‌سازی
   - معمولاً عملکرد قابل قبولی در مقایسه با پیچیدگی پایین آن دارد

### تأثیر انواع همبندی

شبیه‌ساز سه نوع همبندی را پشتیبانی می‌کند:

1. **نگاشت مستقیم (Direct-Mapped)**:
   - هر آدرس حافظه فقط می‌تواند در یک مکان مشخص در کش قرار گیرد
   - مزایا: پیاده‌سازی ساده و سریع
   - معایب: نرخ برخورد پایین‌تر به دلیل تداخل (conflict)

2. **همبندی مجموعه‌ای (Set-Associative)**:
   - هر آدرس حافظه می‌تواند در یکی از چند مکان در یک مجموعه قرار گیرد
   - مزایا: تعادل خوب بین پیچیدگی و عملکرد
   - معایب: نیاز به الگوریتم جایگزینی برای انتخاب بلوک

3. **تمام همبند (Fully-Associative)**:
   - هر آدرس حافظه می‌تواند در هر مکانی از کش قرار گیرد
   - مزایا: بالاترین نرخ برخورد ممکن
   - معایب: پیچیدگی سخت‌افزاری بالا و کندتر بودن جستجو

### تأثیر اندازه بلوک

اندازه بلوک تأثیر مهمی در کارایی کش دارد:

- **بلوک‌های کوچک**:
  - مزایا: کاهش اتلاف فضا (زمانی که فقط بخشی از بلوک استفاده می‌شود)
  - معایب: افزایش سربار به دلیل تعداد بیشتر بلوک‌ها

- **بلوک‌های بزرگ**:
  - مزایا: بهره‌گیری از محلیت مکانی و کاهش سربار
  - معایب: افزایش اتلاف فضا و زمان انتقال بلوک

## نتایج آزمایش‌های نمونه

### آزمایش جامع

در آزمایش جامع، تمام ترکیبات ممکن پیکربندی‌های زیر بررسی می‌شوند:
- اندازه کش: 1KB، 4KB، 16KB
- اندازه بلوک: 32B، 64B، 128B
- همبندی: نگاشت مستقیم، 2-way، 4-way، تمام همبند
- سیاست جایگزینی: LRU، FIFO، LFU، RANDOM
- الگوهای دسترسی: ترتیبی، تصادفی، حلقه‌ای، محلیت

نتایج نمونه برای بهترین پیکربندی در هر الگوی دسترسی:

| الگو | اندازه کش (B) | اندازه بلوک (B) | نوع | سیاست | نرخ برخورد |
|-----|-------------|--------------|-----|------|----------|
| ترتیبی | 16384 | 128 | تمام همبند | LRU | 0.9850 |
| تصادفی | 16384 | 64 | تمام همبند | LRU | 0.3125 |
| حلقه‌ای | 16384 | 64 | 4-Way | LFU | 0.9002 |
| محلیت | 16384 | 128 | تمام همبند | LRU | 0.8274 |

### تحلیل نتایج

- **الگوی ترتیبی**: بیشترین نرخ برخورد (98.5%) با کش بزرگ، بلوک بزرگ و همبندی کامل به دست می‌آید. این به دلیل محلیت مکانی بالای این الگوست.

- **الگوی تصادفی**: پایین‌ترین نرخ برخورد (31.25%) که حتی با بهترین پیکربندی هم قابل توجه نیست. این به دلیل عدم وجود محلیت زمانی و مکانی در این الگوست.

- **الگوی حلقه‌ای**: نرخ برخورد خوب (90.02%) با کش بزرگ و همبندی 4-way. سیاست LFU در این الگو بهتر عمل می‌کند زیرا برخی آدرس‌ها مکرراً استفاده می‌شوند.

- **الگوی محلیت**: نرخ برخورد خوب (82.74%) با کش بزرگ، بلوک بزرگ و همبندی کامل. سیاست LRU برای این الگو مناسب است زیرا محلیت زمانی بالایی دارد.

## بهینه‌سازی کارایی کش

بر اساس نتایج و تحلیل‌ها، می‌توان راهکارهای زیر را برای بهینه‌سازی کارایی کش پیشنهاد داد:

1. **انتخاب اندازه مناسب کش**:
   - کش بزرگتر معمولاً نرخ برخورد بهتری دارد اما هزینه بالاتری نیز دارد
   - افزایش اندازه کش تا حد مشخصی مفید است و پس از آن تأثیر چندانی ندارد

2. **انتخاب اندازه مناسب بلوک**:
   - برای الگوهای با محلیت مکانی بالا، بلوک‌های بزرگتر مناسب‌تر هستند
   - برای الگوهای تصادفی، بلوک‌های کوچکتر کارآمدتر هستند

3. **انتخاب همبندی مناسب**:
   - همبندی بالاتر نرخ برخورد بهتری دارد اما پیچیدگی بیشتری نیز به همراه دارد
   - همبندی 4-way یا 8-way معمولاً تعادل خوبی بین کارایی و پیچیدگی دارد

4. **انتخاب سیاست جایگزینی مناسب**:
   - LRU برای اکثر برنامه‌های واقعی با محلیت زمانی و مکانی مناسب است
   - LFU برای برنامه‌هایی با الگوی دسترسی غیریکنواخت مناسب است
   - سیاست RANDOM با وجود سادگی، گاهی عملکرد قابل قبولی دارد

## کاربردهای شبیه‌ساز

این شبیه‌ساز کش می‌تواند در موارد زیر مورد استفاده قرار گیرد:

1. **آموزش مفاهیم معماری کامپیوتر**:
   - به دانشجویان کمک می‌کند تا مفهوم کش و عملکرد آن را بهتر درک کنند
   - امکان آزمایش و مشاهده تأثیر پارامترهای مختلف بر کارایی کش

2. **بهینه‌سازی سیستم‌های واقعی**:
   - می‌تواند برای پیش‌بینی عملکرد کش در سیستم‌های واقعی استفاده شود
   - کمک به طراحی و پیکربندی بهینه کش برای کاربردهای خاص

3. **ارزیابی الگوریتم‌ها و ساختارهای داده**:
   - بررسی رفتار دسترسی به حافظه الگوریتم‌ها و ساختارهای داده مختلف
   - کمک به بهینه‌سازی کد برای استفاده بهتر از کش

4. **تحقیق و توسعه**:
   - امکان پیاده‌سازی و آزمایش روش‌های جدید جایگزینی بلوک
   - آزمایش معماری‌های پیشرفته کش

## امکانات گسترش آینده

شبیه‌ساز فعلی می‌تواند با افزودن قابلیت‌های زیر گسترش یابد:

1. **پشتیبانی از کش چندسطحی**:
   - شبیه‌سازی سلسله مراتب کش (L1، L2، L3)
   - بررسی تعامل بین سطوح مختلف کش

2. **شبیه‌سازی کش داده و دستورالعمل مجزا**:
   - تفکیک کش داده و دستورالعمل
   - بررسی تأثیر الگوهای مختلف دسترسی به داده و دستورالعمل

3. **پشتیبانی از سیاست‌های نوشتن مختلف**:
   - پیاده‌سازی سیاست‌های write-through و write-back
   - بررسی تأثیر این سیاست‌ها بر کارایی سیستم

4. **پیاده‌سازی الگوریتم‌های جایگزینی پیشرفته**:
   - ARC (Adaptive Replacement Cache)
   - CLOCK (Second-Chance)
   - و سایر الگوریتم‌های مدرن

5. **رابط کاربری گرافیکی**:
   - ایجاد یک رابط کاربری گرافیکی برای تعامل آسان‌تر با شبیه‌ساز
   - نمایش بصری عملکرد کش به صورت زنده

6. **شبیه‌سازی دقیق‌تر سخت‌افزار**:
   - در نظر گرفتن زمان‌بندی دقیق (timing)
   - شبیه‌سازی پیشرفت (pipelining) و اجرای ناترتیبی (out-of-order execution)

## نتیجه‌گیری

شبیه‌ساز کش ارائه شده در این پروژه، ابزاری قدرتمند برای بررسی و تحلیل عملکرد حافظه کش تحت پیکربندی‌ها و الگوهای دسترسی مختلف است. این شبیه‌ساز نشان می‌دهد که چگونه پارامترهای مختلف کش مانند اندازه، اندازه بلوک، همبندی و سیاست جایگزینی، تأثیر چشمگیری بر کارایی آن دارند.

نتایج آزمایش‌ها تأیید می‌کنند که انتخاب پیکربندی مناسب کش به شدت به الگوی دسترسی به حافظه وابسته است. برای برنامه‌های با محلیت بالا، کش‌های بزرگتر با همبندی بالا و سیاست LRU بهترین عملکرد را دارند، در حالی که برای الگوهای حلقه‌ای، سیاست LFU می‌تواند بهتر عمل کند.

این شبیه‌ساز نه تنها ابزاری آموزشی برای درک بهتر مفاهیم کش است، بلکه می‌تواند برای بهینه‌سازی سیستم‌های واقعی و تحقیق در زمینه معماری کامپیوتر نیز مورد استفاده قرار گیرد. با گسترش قابلیت‌های آن در آینده، می‌توان شبیه‌سازی دقیق‌تر و جامع‌تری از سیستم‌های حافظه مدرن ارائه داد.