local function equal(actual, expected, label)
    assert(table.getn(actual) == table.getn(expected), label .. " length")
    for i = 1, table.getn(expected) do
        assert(actual[i] == expected[i], label .. " field " .. i)
    end
end

for job = 0, 3 do
    for sex = 0, 1 do
        local items = {}
        local completed = 0
        local notices = 0
        local function put(vnum, count, attrs)
            assert(items[vnum] == nil, "duplicate starter item " .. vnum)
            items[vnum] = {count=count, attrs=attrs}
        end
        pc = {
            get_job=function() return job end,
            get_sex=function() return sex end,
            get_name=function() return "fixture" end,
            give_item2=function(vnum, count) put(vnum, count, {}) end,
            make_item0=function(item, sockets, attrs, equip)
                assert(equip == 0)
                assert(table.getn(attrs) <= 10, "maximum five attributes")
                for i = 1, table.getn(attrs), 2 do
                    assert(attrs[i] ~= 21 and attrs[i] ~= 20 and attrs[i] ~= 22,
                           "late-game racial bonus on starter")
                end
                put(item[1], item[2], attrs)
            end,
        }
        notice_all=function(id, name)
            assert(id == 613 and name == "fixture")
            notices = notices + 1
        end
        set_state=function(quest_state)
            assert(quest_state == "__COMPLETE__")
            completed = completed + 1
        end
        local handler = assert(loadfile(WELCOME_FILE))
        handler()
        assert(completed == 1 and notices == 1)
        assert(items[27989] and items[27989].count == 1, "one detector")
        assert(items[76006] == nil and items[8009] == nil)
        local stat = ({5,6,4,4})[job + 1]
        local weapons = {{19,3009},{1009,2009},{19},{5009,7009}}
        local expected = {stat,8,7,5,15,5,16,5,63,10}
        if job == 2 then expected = {4,8,9,10,15,5,16,5,63,10} end
        if job == 3 then expected = {4,8,9,20,15,5,16,5,63,10} end
        for _, vnum in ipairs(weapons[job+1]) do
            assert(items[vnum] and items[vnum].count == 1, "class weapon")
            equal(items[vnum].attrs, expected, "weapon " .. vnum)
        end
        if job == 1 then
            assert(items[8000] and items[8000].count == 200)
        else
            assert(items[8000] == nil)
        end
        equal(items[({11209,11409,11609,11809})[job+1]].attrs,
              {1,1000,9,10,29,10,30,10}, "armor")
        equal(items[({12209,12349,12489,12629})[job+1]].attrs,
              {10,20,11,20,18,10,41,8}, "helmet")
        equal(items[13009].attrs, {stat,8,27,5,18,10}, "shield")
        equal(items[14009].attrs, {1,1000,16,5,18,10}, "bracelet")
        equal(items[16009].attrs, {1,1000,15,5,16,5}, "necklace")
        equal(items[15009].attrs, {1,1000,15,5,8,10}, "shoes")
        equal(items[17009].attrs, {stat,8,8,10,18,10}, "earrings")
        assert(items[sex == 0 and 41003 or 41004])
        assert(items[sex == 0 and 45005 or 45006])
    end
end
print("WELCOME: four classes, both sexes, weapons, legal attributes, arrows and detector PASS")
