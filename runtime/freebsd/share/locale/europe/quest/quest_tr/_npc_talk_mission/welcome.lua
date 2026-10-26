------------------------------------------------
--        Author: Best Studio        		  --
--  Github: https://github.com/ybeststudio    --
------------------------------------------------

quest welcome begin
	state start begin
		when login begin
			-- Normal Metin detector: unlimited use is enforced by CItem::SetSocket.
			pc.give_item2(27989, 1)
			pc.give_item2(52034, 1)
			pc.give_item2(53007, 1)
			pc.give_item2(39120, 1)
			pc.give_item2(72726, 1)
			pc.give_item2(72730, 1)
			pc.give_item2(70038, 1)
			-- permanent_support delivers the 14 permanent items once, including old characters.

			if pc.get_sex() == 0 then
				pc.give_item2(41003, 1)
			elseif pc.get_sex() == 1 then
				pc.give_item2(41004, 1)
			end

			local job = pc.get_job()
			local primary_stat = 5 -- STR / warrior
			if job == 1 then
				primary_stat = 6 -- DEX / ninja
			elseif job == 2 or job == 3 then
				primary_stat = 4 -- INT / sura and shaman
			end
			local weapon_bonus = {primary_stat,8,7,5,15,5,16,5}
			if job == 2 then
				weapon_bonus = {4,8,9,10,15,5,16,5}
			elseif job == 3 then
				weapon_bonus = {4,8,9,20,15,5,16,5}
			end
			local armor_bonus = {1,1000,9,10,29,10,30,10}
			local helm_bonus = {10,20,11,20,18,10,41,8}

			if job == 0 then
				pc.make_item0({19, 1}, {}, weapon_bonus, 0)
				pc.make_item0({3009, 1}, {}, weapon_bonus, 0)
				pc.make_item0({11209, 1}, {28442}, armor_bonus, 0)
				pc.make_item0({12209, 1}, {}, helm_bonus, 0)
			elseif job == 1 then
				pc.make_item0({1009, 1}, {}, weapon_bonus, 0)
				pc.make_item0({2009, 1}, {}, weapon_bonus, 0)
				pc.give_item2(8000, 200)
				pc.make_item0({12349, 1}, {}, helm_bonus, 0)
				pc.make_item0({11409, 1}, {28442}, armor_bonus, 0)
			elseif job == 2 then
				pc.make_item0({19, 1}, {}, weapon_bonus, 0)
				pc.make_item0({11609, 1}, {28442}, armor_bonus, 0)
				pc.make_item0({12489, 1}, {}, helm_bonus, 0)
			elseif job == 3 then
				pc.make_item0({5009, 1}, {}, weapon_bonus, 0)
				pc.make_item0({7009, 1}, {}, weapon_bonus, 0)
				pc.make_item0({11809, 1}, {28442}, armor_bonus, 0)
				pc.make_item0({12629, 1}, {}, helm_bonus, 0)
			end

			pc.make_item0({13009, 1}, {}, {primary_stat,8,27,5,18,10}, 0)
			pc.make_item0({14009, 1}, {}, {1,1000,16,5,18,10}, 0)
			pc.make_item0({16009, 1}, {}, {1,1000,15,5,16,5}, 0)
			pc.make_item0({15009, 1}, {}, {1,1000,15,5,8,10}, 0)
			pc.make_item0({17009, 1}, {}, {primary_stat,8,8,10,18,10}, 0)

			notice_all(613, pc.get_name())
			set_state("__COMPLETE__")
		end
	end

	state __COMPLETE__ begin
	end
end
