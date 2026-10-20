quest midpvp_progression begin
    state start begin
        when 20355.chat."Barones icin hazirlik" with pc.get_level() >= 50 and pc.getqf("barones_ready") == 0 begin
            say_title("Yuzbasi")
            say("Orumcek Zindani 3. kattaki mezar tasini incele, sonra Uriele git.")
            if pc.getqf("barones_step") == 0 then
                if not pc.enough_inventory(71130) then
                    say("Once envanterinde yer ac.")
                    return
                end
                pc.setqf("barones_step", 1)
                pc.give_item2(71130, 1)
            end
        end

        when 20371.chat."Mezar tasini incele" with pc.get_level() >= 50 and pc.get_map_index() == 217 and pc.getqf("barones_step") == 1 begin
            say_title("Mezar Tasi")
            say("Izleri inceledin. Uriel sana Arachnida Anahtarini ogretebilir.")
            pc.setqf("barones_step", 2)
        end

        when 20001.chat."Barones hazirligini tamamla" with pc.get_level() >= 50 and pc.getqf("barones_step") == 2 and pc.getqf("barones_ready") == 0 begin
            say_title("Uriel")
            say("Artik zehir ve orumcek malzemelerini getirerek anahtar uretebilirsin.")
            pc.setqf("barones_ready", 1)
            pc.setqf("barones_step", 3)
        end

        when 20001.chat."Arachnida Anahtari uret" with pc.get_level() >= 50 and pc.getqf("barones_ready") == 1 begin
            say_title("Uriel")
            say("Her malzemeden birer adet gerekir. Uretim basarisi yuzde 100.")
            say("Kralice zehri, zehir kesesi, ag, gozler, yumurta kesesi ve bacaklar.")
            if select("Uret", "Vazgec") ~= 1 then return end
            local materials = {30326, 30025, 30056, 30057, 30058, 30059}
            for i, vnum in ipairs(materials) do
                if pc.count_item(vnum) < 1 then
                    say("Eksik malzeme:")
                    say_item_vnum(vnum, 1)
                    return
                end
            end
            if not pc.enough_inventory(30324) then
                say("Once envanterinde yer ac.")
                return
            end
            for i, vnum in ipairs(materials) do pc.remove_item(vnum, 1) end
            pc.give_item2(30324, 1)
            say("Arachnida Anahtarin hazir. Her giriste bir anahtar kullanilir.")
        end
    end
end
