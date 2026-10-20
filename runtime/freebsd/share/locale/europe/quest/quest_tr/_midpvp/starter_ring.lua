-- Separate delivery also covers characters that already completed welcome.
quest starter_ring begin
    state start begin
        function deliver()
            if pc.count_item(40004) > 0 then
                set_state("__COMPLETE__")
                return
            end
            if pc.get_empty_inventory_count() < 1 then
                syschat("Isinlanma yuzugu icin envanterinde bir yer ac. Saticidan teslim alabilirsin.")
                return
            end
            pc.give_item2(40004, 1)
            if pc.count_item(40004) > 0 then
                set_state("__COMPLETE__")
                syschat("Isinlanma yuzugun envanterine eklendi. Sag tiklayarak kullanabilirsin.")
            end
        end

        when login begin
            timer("starter_ring_delivery", 3)
        end

        when starter_ring_delivery.timer begin
            starter_ring.deliver()
        end

        when 9003.chat."Isinlanma yuzugumu al" begin
            starter_ring.deliver()
        end
    end

    state __COMPLETE__ begin
    end
end
