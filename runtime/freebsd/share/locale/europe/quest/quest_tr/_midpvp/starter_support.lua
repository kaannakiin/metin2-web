-- Support skills and a permanent military horse; main class skills stay earned.
quest starter_support begin
    state start begin
        function repair_detector()
            if pc.getqf("detector_recovery_v1") == 1 then
                return
            end
            if pc.count_item(27989) == 0 and pc.get_empty_inventory_count() > 0 then
                pc.give_item2(27989, 1)
            end
            if pc.count_item(27989) > 0 then
                pc.setqf("detector_recovery_v1", 1)
            end
        end

        function apply()
            -- Repair old characters even when the book was already delivered.
            if horse.get_level() < 30 then
                horse.set_level(30)
            end
            if pc.getqf("horse_ready") == 0 then
                if horse.is_dead() then
                    horse.revive()
                end
                horse.feed()
                if pc.count_item(50053) == 0 and pc.get_empty_inventory_count() > 0 then
                    pc.give_item2(50053, 1)
                end
                if pc.count_item(50053) > 0 then
                    pc.setqf("horse_ready", 1)
                    syschat("Kalici askeri atin ve cagirma kitabin hazir.")
                end
            end

            if pc.get_level() < 5 then
                return
            end
            -- Skill 130 follows horse level. Languages and combo use their
            -- own caps. Call Horse 10 already gives the full summon chance.
            local skills = {{121,40},{122,2},{124,40},{126,20},{127,20},
                            {128,20},{129,40},{130,30},{131,10},{137,40},{138,40},
                            {139,40},{140,40}}
            for index = 1, table.getn(skills) do
                if pc.get_skill_level(skills[index][1]) < skills[index][2] then
                    pc.set_skill_level(skills[index][1], skills[index][2])
                end
            end
        end

        when login begin
            starter_support.apply()
            loop_timer("starter_support_refresh", 5)
        end

        when levelup begin
            starter_support.apply()
        end

        when starter_support_refresh.timer begin
            starter_support.apply()
            -- Wait until all first-login gifts have run to avoid duplicates.
            starter_support.repair_detector()
            -- Also restores support skills after an in-session class reset.
        end

        when 20349.chat."Kalici atimi ve becerilerimi hazirla" begin
            starter_support.apply()
        end
    end
end
