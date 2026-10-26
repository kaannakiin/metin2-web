local handler = assert(loadfile(WELCOME_FILE))
local items, flags, free, grants = {}, {}, 0, 0
pc = {
    getqf = function(k) return flags[k] or 0 end,
    setqf = function(k,v) flags[k]=v end,
    count_item = function(k) return items[k] or 0 end,
    get_empty_inventory_count = function() return free end,
    give_item2 = function(k,n)
        assert(n==1 and free>0)
        free=free-1; items[k]=(items[k] or 0)+1; grants=grants+1
        return grants
    end,
}
handler(); assert(grants==0)
free=5; handler(); assert(grants==5)
handler(); assert(grants==5)
free=50; handler(); assert(grants==14)
handler(); assert(grants==14)
items[72737]=0; handler(); assert(grants==14)
items={ [72731]=1 }; flags={}; grants=0; free=50
handler(); assert(grants==13 and items[72731]==1)
print('PASS: full inventory, partial retry, all 14, no repeated grant, existing permanent item')
