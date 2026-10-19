------------------------------------------------
-- Mid-easy 1-99 PvP participation rewards
-- Yang + skill books only (no power gear).
-- Enable claim window: /e mid_pvp_pay 1
-- Disable:            /e mid_pvp_pay 0
------------------------------------------------

quest mid_pvp_rewards begin
	state start begin
		when letter begin
			if game.get_event_flag("mid_pvp_pay") ~= 0 then
				local day = math.floor(get_global_time() / 86400)
				if pc.getf("mid_pvp_rewards", "day") ~= day then
					setskin(NOWINDOW)
					makequestbutton("PvP katılım ödülü")
				end
			end
		end

		when button begin
			if game.get_event_flag("mid_pvp_pay") == 0 then
				say("Ödül şu an kapalı.")
				return
			end

			local day = math.floor(get_global_time() / 86400)
			if pc.getf("mid_pvp_rewards", "day") == day then
				say("Bugünkü PvP ödülünü zaten aldın.")
				return
			end

			-- 500.000 yang + 3 beceri kitabı (50300)
			pc.give_gold(500000)
			pc.give_item2(50300, 3)
			pc.setf("mid_pvp_rewards", "day", day)
			say("Ödül: 500.000 yang ve 3 beceri kitabı. İyi savaşlar!")
		end
	end
end
