// Exercise the production transition code without a database or game process.
#include <algorithm>
#include <array>
#include <cassert>
#include <iostream>
#include <list>
#include <vector>
#define __INC_METIN_II_GAME_CONSTANTS_H__
enum { ITEM_ARMOR=2, ITEM_COSTUME=28, ITEM_RING=33, ITEM_DS=29, ITEM_SPECIAL_DS=30,
       ITEM_GROWTH_PET=36, ITEM_PASSIVE=38, ARMOR_BELT=7, COSTUME_BODY=0, COSTUME_WEAPON=3,
       AFFECT_BLEND=500, AFFECT_MALL=501, AFFECT_BLEND_PLUS=550, AFFECT_MALL_PLUS=549,
       AFFECT_ATT_SPEED=201, AFFECT_MOV_SPEED=202, AFFECT_UNIQUE_ABILITY=203,
       MAX_APPLY_NUM=150, INVENTORY_MAX_NUM=90, INFINITE_AFFECT_DURATION=1892160000 };
struct Apply { unsigned bPointType; } aApplyInfo[MAX_APPLY_NUM];
struct CAffect { unsigned type, point; int value; };
struct Item {
    unsigned vnum; int apply, value, socket=0; bool locked=false;
    unsigned GetVnum() const {return vnum;}
    int GetValue(int i) const {return i == 0 ? apply : value;}
    int GetSocket(int) const {return socket;}
    void SetSocket(int,int value) {socket=value;}
    void Lock(bool value) {locked=value;}
};
using LPITEM=Item*;
struct CHARACTER {
    bool dead=false, loaded=true;
    std::list<CAffect> effects;
    std::array<LPITEM,INVENTORY_MAX_NUM> items={};
    bool IsDead() const {return dead;}
    bool IsLoadedAffect() const {return loaded;}
    CAffect* FindAffect(unsigned type,unsigned point) {
        for(auto& e:effects) if(e.type==type && e.point==point) return &e;
        return nullptr;
    }
    void RemoveAffect(CAffect* e) {effects.remove_if([e](const CAffect& x){return &x==e;});}
    void RemoveAffect(unsigned type) {effects.remove_if([type](const CAffect& x){return x.type==type;});}
    bool AddAffect(unsigned type,unsigned point,int value,int,int,int,bool) {
        effects.push_back({type,point,value}); return true;
    }
    LPITEM GetInventoryItem(unsigned cell) {return items[cell];}
};
#include "../../apps/server/game/src/pvp_support.h"
struct Proto {
    unsigned dwVnum=0,dwVnumRange=0,dwFlags=4,bSubType=0;
    struct Limit {unsigned bType=0;int lValue=0;} aLimits[2];
    int alValues[6]={};
};
int main() {
    for(unsigned i=0;i<MAX_APPLY_NUM;++i) aApplyInfo[i].bPointType=i;
    Proto p; p.dwVnum=72737; pvp_support::Configure(p,34,1);
    assert(p.alValues[0]==7 && p.alValues[1]==30 && p.alValues[2]==1);
    assert(p.aLimits[0].lValue==1 && p.dwFlags==0);
    p.dwVnum=72738; pvp_support::Configure(p,34,1);
    assert(p.alValues[0]==8 && p.alValues[1]==40);
    p.dwVnum=50827; p.aLimits[0].lValue=55; pvp_support::Configure(p,34,1);
    assert(p.aLimits[0].lValue==1);
    CHARACTER ch;
    Item green{72737,7,30}, yellow{50829,7,8}, copy{72737,7,30};
    ch.items[0]=&green; ch.items[1]=&yellow; ch.items[2]=&copy;
    ch.AddAffect(AFFECT_ATT_SPEED,7,30,0,600,0,false);
    assert(pvp_support::Toggle(&ch,&green));
    assert(!ch.FindAffect(AFFECT_ATT_SPEED,7) && ch.FindAffect(AFFECT_MALL_PLUS,7)->value==30);
    assert(green.locked && green.socket==1);
    assert(!pvp_support::Toggle(&ch,&copy));
    assert(pvp_support::Toggle(&ch,&yellow));
    assert(ch.effects.size()==2); // Yellow dew and green potion are separate families.
    assert(pvp_support::Toggle(&ch,&green));
    assert(!green.locked && green.socket==0 && ch.effects.size()==1);
    assert(pvp_support::Toggle(&ch,&green));
    copy.socket=1; // Simulate old duplicated active sockets and an orphan DB bonus.
    ch.AddAffect(AFFECT_MALL_PLUS,16,999,0,50,0,false);
    pvp_support::Restore(&ch);
    assert(ch.effects.size()==2 && copy.socket==0 && !copy.locked);
    pvp_support::Restore(&ch);
    assert(ch.effects.size()==2 && green.locked && yellow.locked);
    green.socket=0; pvp_support::Restore(&ch);
    assert(ch.effects.size()==1 && !green.locked);
    ch.items[1]=nullptr; pvp_support::Restore(&ch);
    assert(ch.effects.empty());
    ch.dead=true; assert(!pvp_support::Toggle(&ch,&green));
    ch.dead=false; ch.loaded=false; assert(!pvp_support::Toggle(&ch,&green));
    assert(pvp_support::PermanentAffect(AFFECT_MALL_PLUS));
    assert(!pvp_support::PermanentAffect(AFFECT_ATT_SPEED));
    assert(pvp_support::DisabledEquipment(ITEM_ARMOR,8));
    assert(!pvp_support::DisabledEquipment(ITEM_ARMOR,6));
    assert(pvp_support::DisabledEquipment(ITEM_COSTUME,1));
    assert(!pvp_support::DisabledEquipment(ITEM_COSTUME,3));
    std::cout << "PASS: limits, speed values, toggle, duplicate, temporary replacement, relog, orphan, death guard, equipment policy\n";
}
