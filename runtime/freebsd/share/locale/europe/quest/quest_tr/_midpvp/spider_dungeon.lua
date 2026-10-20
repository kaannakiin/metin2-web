-- Active mid-easy profile. Baseline: quest_tr/_alldungeons/spider_dungeon.lua
------------------------------------------------
--        Author: Best Studio        		  --
--  Github: https://github.com/ybeststudio    --
------------------------------------------------
-- NOT: Bu dosya Unix (LF) line ending ve Windows-1254 (Turkce ANSI) encoding ile kaydedilmelidir
-- Encoding: Windows-1254 (Turkce ANSI) - Turkce karakterleri destekler
-- Line Ending: LF (Unix formati)
------------------------------------------------

quest spider_dungeon begin
	state start begin
        when 20371.chat."Barones'in Yuvasi" with pc.get_map_index() == 217 begin
            say_title("Zindan girisi")
            say("Gerekli seviye: 50. Gunluk giris kotasi yok.")
            local choice = select("Yalniz", "Grupla", "Vazgec")
            if choice == 3 then return end
            if not (pc.get_level() >= 50 and pc.getf("midpvp_progression", "barones_ready") == 1 and (pc.is_gm() or pc.getf("spider_dungeon", "cooldown") <= get_global_time())) or not (pc.count_item(30324) >= 1) then
                say("Seviye, hazirlik, anahtar veya bekleme kosulu eksik.")
                return
            end
            if choice == 1 then
                if party.is_party() then
                    say("Tek basina girmek icin once gruptan ayril.")
                    return
                end
                pc.remove_item(30324, 1)
                d.new_jump(217, 88100, 614800)
            else
                if not party.is_party() or not party.is_leader() then
                    say("Grup lideri girisi baslatmali.")
                    return
                end
                local pids = {party.get_member_pids()}
                local origin = pc.get_map_index()
                local ready = party.get_near_count() == table.getn(pids)
                for i, pid in ipairs(pids) do
                    q.begin_other_pc_block(pid)
                    if pc.get_map_index() ~= origin or not (pc.get_level() >= 50 and pc.getf("midpvp_progression", "barones_ready") == 1 and (pc.is_gm() or pc.getf("spider_dungeon", "cooldown") <= get_global_time())) or not (pc.count_item(30324) >= 1) then
                        ready = false
                    end
                    q.end_other_pc_block()
                end
                if not ready then
                    say("Tum uyeler yaninda olmali ve giris kosullarini tamamlamali.")
                    return
                end
                -- Each member pays once below.
                for i, pid in ipairs(pids) do
                    q.begin_other_pc_block(pid)
                    pc.remove_item(30324, 1)
                    q.end_other_pc_block()
                end
                d.new_jump_party(217, 881, 6148)
            end
            if d.select(d.get_map_index()) then
                d.setf("first_regen", 1)
                d.setf("DungeonBlock", 1)
            end
        end

		when barones_1.server_timer begin
			local arg = get_server_timer_arg()
			if d.select(arg) then
				if d.getf("first_regen") == 1 then
					d.setf("first_regen", 0)
                    d.spawn_name_mob(2094, 367, 588, "Orumcek Baronu")
                    d.setf("baron_dead", 0)
                    d.setf("barones_spawned", 0)
					d.notice(arg, 674, "", false)

					GetMissionInfo(1, 20*60)

					d.setf("real_time", get_global_time()+20*60)
					d.setf("DungeonBlock", 1)
					server_timer("spider_full_timer", 60*20, arg)
				end
			end
		end

		when spider_full_timer.server_timer begin
			local index = get_server_timer_arg()
			if d.select(index) then
				d.purge()
				d.setf("DungeonBlock", 0)
				d.global_warp_all_to_base(689*100, 6111*100, index, 1)
			end
		end

        when 2094.kill with pc.get_map_index() >= 2170000 and pc.get_map_index() <= 2179990 begin
            if d.select(pc.get_map_index()) and d.getf("baron_dead") == 0 then
                d.setf("baron_dead", 1)
                game.drop_item_with_ownership(30327, 1)
                chat("Arachnida Flutu ile Baronesi cagir.")
            end
        end

        when 30327.use with pc.get_map_index() >= 2170000 and pc.get_map_index() <= 2179990 begin
            if d.select(pc.get_map_index()) and d.getf("baron_dead") == 1 and d.getf("barones_spawned") == 0 then
                if pc.count_item(30327) < 1 then return end
                d.setf("barones_spawned", 1)
                pc.remove_item(30327, 1)
					d.spawn_mob(2095, 400, 566)
					d.spawn_mob(2095, 400, 594)
					d.spawn_mob(2095, 362, 600)
					d.spawn_mob(2095, 337, 599)
					d.spawn_mob(2095, 335, 581)
					d.spawn_mob(2095, 344, 562)
					d.spawn_mob(2095, 364, 588)
					d.spawn_mob(2095, 379, 562)
					d.spawn_mob(2095, 368, 525)

					local kingVid = d.spawn_mob(2092, 367, 588)
					d.setf("king_vid", kingVid)
					d.setf("remain_egg", 9)
                GetMissionInfo(2, 20*60)
            end
        end

		when 2095.kill with pc.get_map_index() >= 2170000 and pc.get_map_index() <= 2179990 begin
			if d.select(pc.get_map_index()) then
				d.notice(pc.get_map_index(), 675, "", false)
				d.notice(pc.get_map_index(), 676, "", false)
				local kingVid = d.getf("king_vid")
				local remain_egg = d.getf("remain_egg")
				d.setf("remain_egg", remain_egg-1)
				npc.set_vid_attack_mul(kingVid, 3/(remain_egg + 1))
				npc.set_vid_damage_mul(kingVid, 10/(remain_egg + 1))
			end
		end

		when 2092.kill with pc.get_map_index() >= 2170000 and pc.get_map_index() <= 2179990 begin
			server_timer("spider_barones_dead_timer", 1, d.get_map_index())
			d.spawn_mob(30130, pc.get_local_x()-5, pc.get_local_y()+5)
			d.setf("dungeon_empire", pc.get_empire())
		end

		when spider_barones_dead_timer.server_timer begin
			local arg = get_server_timer_arg()
			if d.select(arg) then
				if d.getf("DungeonBlock") == 1 then
					GetMissionInfo(1, 60)
					d.global_warp_all_to_base(68900, 611100, arg, 60)
					d.notice(arg, 673, "", false)
					d.setqf2("spider_dungeon", "cooldown", get_global_time()+10*60)

					--Track Window Dungeon Status
					d.track_update(2092)

					d.setf("level", 0)
					d.setf("king_vid", 0)
					d.setf("remain_egg", 0)
					d.setf("real_time", 0)
					d.setf("DungeonBlock",0)
					clear_server_timer("spider_full_timer", arg)
					clear_server_timer("barones_1", arg)
				end
			end
		end

		when logout with pc.get_map_index() >= 2170000 and pc.get_map_index() <= 2179990 begin
			if d.getf("DungeonBlock") == 1 then
				pc.setf("spider_dungeon", "map", d.get_map_index())
				pc.setf("spider_dungeon", "time", get_global_time()+15*60)
				pc.setf("spider_dungeon", "channel", pc.get_channel_id())
			else
				pc.setf("spider_dungeon", "map", 0)
				pc.setf("spider_dungeon", "time", 0)
				pc.setf("spider_dungeon", "channel", 0)
			end
		end

		when login with pc.get_map_index() >= 2170000 and pc.get_map_index() <= 2179990 begin
			pc.set_warp_location_local(217, 689, 6111)
			local index = d.get_map_index()
			if index >= 2170000 and index <= 2179990 then
				if d.getf("DungeonBlock") == 1 then
					if d.getf("first_regen") == 1 then
						server_timer("barones_1", 1, index)
					end
				else
					pc.warp(68900, 611100)
				end
				cmdchat(string.format("RefreshDungeonTimer %d %d", d.getf("level"), d.getf("real_time") - get_global_time()))
			end
		end

		when 20371.chat."Geri don..." with pc.getf("spider_dungeon", "map") >= 1 begin
			local dungeonChannel = pc.getf("spider_dungeon", "channel")

			if pc.get_channel_id() == dungeonChannel then
				local dungeonMapIndex = pc.getf("spider_dungeon", "map")

				if d.select(dungeonMapIndex) then
					local dwLevel = d.getf_from_map_index("level", dungeonMapIndex)
					local ticket = d.getf_from_map_index("ticket", dungeonMapIndex)

					if get_global_time() > pc.getf("spider_dungeon", "time") then
						say_new("[ENTER]Geri donmek icin 15 dakikaniz vardi! [ENTER]")
						pc.setf("spider_dungeon", "map", 0)
						pc.setf("spider_dungeon", "time", 0)
						pc.setf("spider_dungeon", "channel", 0)
						return
					end
					pc.warp(881*100, 6148*100, dungeonMapIndex)
				else
					say_new("Musait degil, tekrar baslayabilirsiniz. [ENTER]")
					pc.setf("spider_dungeon", "map", 0)
					pc.setf("spider_dungeon", "time", 0)
					pc.setf("spider_dungeon", "channel", 0)
				end
			else
				say_new("Zindan bu kanalda acilmadi! [ENTER]")
				say_new(string.format("Girmek icin, %d kanalina gidin. [ENTER]", dungeonChannel))
				return
			end
		end
	end
end
