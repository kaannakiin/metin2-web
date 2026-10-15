USE player;

-- Rows tagged "-- approx" are reconstructed or estimated. SP costs, cooldowns, splash ranges and
-- durations are estimates on every row. bMaxLevel is 1 for job skills (k = skill_power * bMaxLevel / 100).

SET @AFF_BOHO = 24;
SET @AFF_CHEONGEUN = 17;
SET @AFF_CHEONUN = 58;
SET @AFF_EUNHYUNG = 19;
SET @AFF_GEOMGYEONG = 16;
SET @AFF_GICHEON = 30;
SET @AFF_GWIGUM = 20;
SET @AFF_GYEONGGONG = 18;
SET @AFF_HOSIN = 23;
SET @AFF_JEONGWIHON = 15;
SET @AFF_JEUNGRYEOK = 31;
SET @AFF_JUMAGAP = 22;
SET @AFF_KWAESOK = 25;
SET @AFF_MANASHIELD = 26;
SET @AFF_MUYEONG = 27;
SET @AFF_TERROR = 21;

REPLACE INTO `skill_proto` (dwVnum,szName,bType,bMaxLevel,dwSplashRange,szPointOn,szPointPoly,szSPCostPoly,szDurationPoly,szDurationSPCostPoly,szCooldownPoly,szMasterBonusPoly,setFlag,setAffectFlag,szPointOn2,szPointPoly2,szDurationPoly2,setAffectFlag2,szPointOn3,szPointPoly3,szDurationPoly3,szGrandMasterAddSPCostPoly,bLevelStep,bLevelLimit,prerequisiteSkillVnum,prerequisiteSkillLevel,iMaxHit,szSplashAroundDamageAdjustPoly,eSkillType,dwTargetRange) VALUES
(1,'Three-Way Cut',1,1,200,'HP','-(1.1*atk+(0.1*atk+1.5*str)*k)','40+100*k','0','0','12','-(1.1*atk+(0.1*atk+1.5*str)*k)','ATTACK,USE_MELEE_DAMAGE,SPLASH',0,'NONE','0','0',0,'','0','0','40+100*k',1,0,0,0,0,'1','MELEE',0),
(2,'Sword Spin',1,1,350,'HP','-(3*atk+(0.8*atk+6*str+2*dex+con)*k)','60+150*k','0','0','18','-(3*atk+(0.8*atk+6*str+2*dex+con)*k)','ATTACK,USE_MELEE_DAMAGE,SELFONLY,SPLASH,CRUSH',0,'NONE','0','0',0,'','0','0','60+150*k',1,0,0,0,0,'1','MELEE',0),
(3,'Berserk',1,1,0,'ATT_SPEED','50*k','30+30*k','3600','1+3*k','3','50*k','SELFONLY,TOGGLE',@AFF_JEONGWIHON,'MOV_SPEED','20*k','3600',0,'','0','0','30+30*k',1,0,0,0,0,'1','NORMAL',0),
(4,'Aura of the Sword',1,1,0,'ATT_GRADE','(100+str)*k','40+60*k','3600','1+2*k','3','(100+str)*k','SELFONLY,TOGGLE',@AFF_GEOMGYEONG,'NONE','0','0',0,'','0','0','40+60*k',1,0,0,0,0,'1','NORMAL',0),
(5,'Dash',1,1,250,'HP','-(2*atk+(atk+3*dex+7*str+con)*k)','60+160*k','0','0','15','-(2*atk+(atk+3*dex+7*str+con)*k)','ATTACK,USE_MELEE_DAMAGE,SPLASH,CRUSH',0,'MOV_SPEED','0','5',0,'','0','0','60+160*k',1,0,0,0,0,'1','MELEE',0),
(6,'Life Will',1,1,250,'HP','-((3*atk+(atk+1.5*str)*k)*1.07)','70+180*k','0','0','15','-((3*atk+(atk+1.5*str)*k)*1.07)','ATTACK,USE_MELEE_DAMAGE,SPLASH',0,'NONE','0','0',0,'','0','0','70+180*k',1,0,0,0,0,'1','MELEE',0), -- approx
(16,'Spirit Strike (W)',1,1,250,'HP','-(2.3*atk+(4*atk+4*str+con)*k)','70+170*k','0','0','10','-(2.3*atk+(4*atk+4*str+con)*k)','ATTACK,USE_MELEE_DAMAGE,SPLASH,CRUSH',0,'NONE','0','0',0,'','0','0','70+170*k',1,0,0,0,0,'1','MELEE',0),
(17,'Bash',1,1,250,'HP','-(2.3*atk+(3*atk+4*str+3*con)*k)','70+170*k','0','0','14','-(2.3*atk+(3*atk+4*str+3*con)*k)','ATTACK,USE_MELEE_DAMAGE,SPLASH',0,'NONE','0','0',0,'','0','0','70+170*k',1,0,0,0,0,'1','MELEE',0),
(18,'Stump',1,1,400,'HP','-(2*atk+(2*atk+2*dex+2*con+4*str)*k)','80+200*k','0','0','20','-(2*atk+(2*atk+2*dex+2*con+4*str)*k)','ATTACK,USE_MELEE_DAMAGE,SELFONLY,SPLASH,STUN',0,'NONE','(100+1000*k/6)/10','2',0,'','0','0','80+200*k',1,0,0,0,0,'1','MELEE',0),
(19,'Strong Body',1,1,0,'DEF_GRADE','7+(40+0.2*str+0.4*con)*k','40+60*k','3600','1+2*k','3','7+(40+0.2*str+0.4*con)*k','SELFONLY,TOGGLE',@AFF_CHEONGEUN,'MOV_SPEED','-(1+9*k)','3600',0,'','0','0','40+60*k',1,0,0,0,0,'1','NORMAL',0),
(20,'Sword Strike',1,1,500,'HP','-(2*atk+(atk+dex*3+str*5+con)*k)','80+180*k','0','0','14','-(2*atk+(atk+dex*3+str*5+con)*k)','ATTACK,USE_MELEE_DAMAGE,SELFONLY,SPLASH,STUN,CRUSH,WIND',0,'NONE','(100+k*1000/6)/10','2',0,'','0','0','80+180*k',1,0,0,0,0,'1','RANGE',0),
(21,'Sword Circle',1,1,400,'HP','-((2*atk+(2*atk+2*dex+2*con+str*4)*k)*1.1)','90+200*k','0','0','20','-((2*atk+(2*atk+2*dex+2*con+str*4)*k)*1.1)','ATTACK,USE_MELEE_DAMAGE,SELFONLY,SPLASH',0,'NONE','0','0',0,'','0','0','90+200*k',1,0,0,0,0,'1','MELEE',0), -- approx
(31,'Ambush',2,1,0,'HP','-(atk+(1.2*atk+number(500,700)+dex*12)*k)','40+100*k','0','0','10','-(atk+(1.2*atk+number(500,700)+dex*12)*k)','ATTACK,USE_MELEE_DAMAGE',0,'NONE','0','0',0,'','0','0','40+100*k',1,0,0,0,0,'1','MELEE',0),
(32,'Fast Attack',2,1,0,'HP','-(atk+(1.6*atk+number(200,300)+dex*7+str*7)*k)','60+140*k','0','0','12','-(atk+(1.6*atk+number(200,300)+dex*7+str*7)*k)','ATTACK,USE_MELEE_DAMAGE',0,'NONE','0','0',0,'','0','0','60+140*k',1,0,0,0,0,'1','RANGE',0),
(33,'Rolling Dagger',2,1,300,'HP','-(2*atk+(0.5*atk+dex*9+str*7)*k)','60+150*k','0','0','15','-(2*atk+(0.5*atk+dex*9+str*7)*k)','ATTACK,USE_MELEE_DAMAGE,SELFONLY,SPLASH,POISON',0,'NONE','1+4*k','0',0,'','0','0','60+150*k',1,0,0,0,0,'1','RANGE',0),
(34,'Stealth',2,1,0,'NONE','50*k','30+30*k','600','2+3*k','8','50*k','SELFONLY',@AFF_EUNHYUNG,'NONE','0','0',0,'','0','0','30+30*k',1,0,0,0,0,'1','NORMAL',0), -- approx
(35,'Poisonous Cloud',2,1,300,'HP','-(lv*2+(atk+str*3+dex*18)*k)','70+170*k','0','0','15','-(lv*2+(atk+str*3+dex*18)*k)','ATTACK,USE_MELEE_DAMAGE,SPLASH,POISON',0,'NONE','40*k','0',0,'','0','0','70+170*k',1,0,0,0,0,'1','RANGE',0),
(36,'Insidious Poison',2,1,300,'HP','-((lv*2+(atk+str*3+dex*18)*k)*1.1)','80+200*k','0','0','18','-((lv*2+(atk+str*3+dex*18)*k)*1.1)','ATTACK,USE_MELEE_DAMAGE,SPLASH,POISON',0,'NONE','40*k','0',0,'','0','0','80+200*k',1,0,0,0,0,'1','RANGE',0),
(46,'Repetitive Shot',2,1,0,'HP','-((atk+0.2*atk*floor(2+k*6)+(0.8*atk+dex*8*ar+iq*2)*k)/floor(2+k*6))','60+150*k','0','0','10','-((atk+0.2*atk*floor(2+k*6)+(0.8*atk+dex*8*ar+iq*2)*k)/floor(2+k*6))','ATTACK,USE_ARROW_DAMAGE,CRUSH',0,'NONE','0','0',0,'','0','0','60+150*k',1,0,0,0,0,'1','RANGE',0), -- approx
(47,'Arrow Shower',2,1,400,'HP','-(atk+(1.7*atk+dex*5+str)*k)','70+180*k','0','0','12','-(atk+(1.7*atk+dex*5+str)*k)','ATTACK,SPLASH,USE_ARROW_DAMAGE,SLOW',0,'NONE','20+30*k','8',0,'','0','0','70+180*k',1,0,0,0,0,'1','RANGE',0), -- approx
(48,'Fire Arrow',2,1,250,'HP','-(1.5*atk+(2.6*atk+0.9*iq+number(100,300))*k)','60+160*k','0','0','10','-(1.5*atk+(2.6*atk+0.9*iq+number(100,300))*k)','ATTACK,SPLASH,USE_ARROW_DAMAGE,FIRE_CONT,FIRE',0,'NONE','lv+iq*3*k','(350+iq*4*k)/10',0,'','0','0','60+160*k',1,0,0,0,0,'1','RANGE',0), -- approx
(49,'Feather Walk',2,1,0,'MOV_SPEED','60*k','30+50*k','3600','2+3*k','3','60*k','SELFONLY,TOGGLE',@AFF_GYEONGGONG,'NONE','(lv*2+(3*dex+number(100,300))+str*2+iq*2)*k','0',0,'','0','0','30+50*k',1,0,0,0,0,'1','NORMAL',0), -- approx
(50,'Poison Arrow',2,1,250,'HP','-(atk+(1.4*atk+number(100,200)+dex*7+str*4+iq*4)*k)','70+170*k','0','0','14','-(atk+(1.4*atk+number(100,200)+dex*7+str*4+iq*4)*k)','ATTACK,SPLASH,USE_ARROW_DAMAGE,CRUSH,POISON',0,'NONE','(50+dex*6*k)/10','0',0,'','0','0','70+170*k',1,0,0,0,0,'1','RANGE',0),
(51,'Spark',2,1,350,'HP','-((atk+(1.2*atk+number(100,200)+dex*6+str*3+iq*3)*k)*1.2)','80+200*k','0','0','15','-((atk+(1.2*atk+number(100,200)+dex*6+str*3+iq*3)*k)*1.2)','ATTACK,USE_MELEE_DAMAGE,SELFONLY,SPLASH,POISON',0,'NONE','(50+dex*6*k)/10','0',0,'','0','0','80+200*k',1,0,0,0,0,'1','RANGE',0), -- approx
(61,'Finger Strike',3,1,250,'HP','-(atk+2*lv+iq*2+(2*atk+str*4+iq*14)*k)','50+120*k','0','0','12','-(atk+2*lv+iq*2+(2*atk+str*4+iq*14)*k)','ATTACK,USE_MELEE_DAMAGE,SPLASH,PENETRATE',0,'NONE','1+9*k','0',0,'','0','0','50+120*k',1,0,0,0,0,'1','MELEE',0),
(62,'Dragon Swirl',3,1,350,'HP','-(1.1*atk+2*lv+2*iq+(1.5*atk+str+iq*12)*k)','70+160*k','0','0','15','-(1.1*atk+2*lv+2*iq+(1.5*atk+str+iq*12)*k)','ATTACK,USE_MELEE_DAMAGE,SELFONLY,SPLASH,IGNORE_TARGET_RATING',0,'NONE','1+9*k','0',0,'','0','0','70+160*k',1,0,0,0,0,'1','MELEE',0),
(63,'Enchanted Blade',3,1,0,'ATT_GRADE','7+(5*iq+13)*k','40+60*k','3600','2+4*k','3','7+(5*iq+13)*k','SELFONLY,TOGGLE',@AFF_GWIGUM,'HIT_HP_RECOVER','10*k','3600',0,'','0','0','40+60*k',1,0,0,0,0,'1','NORMAL',0),
(64,'Fear',3,1,0,'NONE','5+20*k','40+60*k','3600','1+3*k','10','5+20*k','SELFONLY,TOGGLE',@AFF_TERROR,'NONE','0','0',0,'','0','0','40+60*k',1,0,0,0,0,'1','NORMAL',0), -- approx
(65,'Enchanted Armour',3,1,0,'DEF_GRADE','(iq+30)*k','50+70*k','3600','2+3*k','3','(iq+30)*k','SELFONLY,TOGGLE',@AFF_JUMAGAP,'REFLECT_MELEE','(iq/4+10)*k','3600',0,'','0','0','50+70*k',1,0,0,0,0,'1','NORMAL',0),
(66,'Dispel',3,1,300,'HP','-(40+5*lv+2*iq+(18*iq+7*mwep+number(50,100))*ar*k)','80+200*k','0','0','15','-(40+5*lv+2*iq+(18*iq+7*mwep+number(50,100))*ar*k)','ATTACK,COMPUTE_MAGIC_DAMAGE,SPLASH,REMOVE_GOOD_AFFECT',0,'NONE','50*k','5',0,'','0','0','80+200*k',1,0,0,0,0,'1','MAGIC',0),
(76,'Dark Strike',3,1,250,'HP','-(40+5*lv+2*iq+(20*iq+7*mwep+number(50,100))*ar*k)','60+150*k','0','0','10','-(40+5*lv+2*iq+(20*iq+7*mwep+number(50,100))*ar*k)','ATTACK,COMPUTE_MAGIC_DAMAGE,SPLASH',0,'NONE','0','0',0,'','0','0','60+150*k',1,0,0,0,0,'1','MAGIC',0),
(77,'Flame Strike',3,1,400,'HP','-(5*lv+2*iq+(20*iq+8*mtk+str*4+con*2+number(180,200))*k)','80+200*k','0','0','16','-(5*lv+2*iq+(20*iq+8*mtk+str*4+con*2+number(180,200))*k)','ATTACK,SELFONLY,COMPUTE_MAGIC_DAMAGE,SPLASH,FIRE',0,'NONE','0','0',0,'','0','0','80+200*k',1,0,0,0,0,'1','MAGIC',0),
(78,'Flame Spirit',3,1,300,'HP','-(30+2*lv+2*iq+(18*iq+6*mwep+number(200,500))*ar*k)','80+100*k','3600','3+5*k','5','-(30+2*lv+2*iq+(18*iq+6*mwep+number(200,500))*ar*k)','ATTACK,COMPUTE_MAGIC_DAMAGE,SPLASH,TOGGLE,FIRE',@AFF_MUYEONG,'NONE','0','0',0,'','0','0','80+100*k',1,0,0,0,0,'1','MAGIC',0),
(79,'Dark Protection',3,1,0,'MANASHIELD','max(10,100-iq*0.6*k)','40+60*k','3600','1+2*k','3','max(10,100-iq*0.6*k)','SELFONLY,TOGGLE',@AFF_MANASHIELD,'DEF_GRADE','(0.5*iq+15)*k','3600',0,'','0','0','40+60*k',1,0,0,0,0,'1','NORMAL',0), -- approx
(80,'Spirit Strike (S)',3,1,300,'HP','-(40+2*lv+2*iq+(2*con+2*dex+22*iq+6*mwep+number(180,200))*ar*k)','80+200*k','0','0','14','-(40+2*lv+2*iq+(2*con+2*dex+22*iq+6*mwep+number(180,200))*ar*k)','ATTACK,COMPUTE_MAGIC_DAMAGE,SPLASH,SLOW',0,'NONE','(333+(300*k))/10','10',0,'','0','0','80+200*k',1,0,0,0,0,'1','MAGIC',0),
(81,'Dark Orb',3,1,300,'HP','-(120+6*lv+(5*con+5*dex+40*iq+12*mwep)*ar*k)','90+220*k','0','0','18','-(120+6*lv+(5*con+5*dex+40*iq+12*mwep)*ar*k)','ATTACK,COMPUTE_MAGIC_DAMAGE,SPLASH',0,'NONE','0','0',0,'','0','0','90+220*k',1,0,0,0,0,'1','MAGIC',0),
(91,'Flying Talisman',4,1,300,'HP','-(70+5*lv+(18*iq+7*str+5*mwep+50)*ar*k)','50+130*k','0','0','10','-(70+5*lv+(18*iq+7*str+5*mwep+50)*ar*k)','ATTACK,COMPUTE_MAGIC_DAMAGE,SPLASH,SLOW',0,'NONE','(3+iq*7*k)/10','10',0,'','0','0','50+130*k',1,0,0,0,0,'1','MAGIC',0),
(92,'Shooting Dragon',4,1,250,'HP','-(60+5*lv+(16*iq+6*dex+6*mwep+120)*ar*k)','60+150*k','0','0','12','-(60+5*lv+(16*iq+6*dex+6*mwep+120)*ar*k)','ATTACK,COMPUTE_MAGIC_DAMAGE,SPLASH,FIRE_CONT,CRUSH,FIRE',0,'NONE','lv+iq*3*k','(100+iq*5*k)/10',0,'','0','0','60+150*k',1,0,0,0,0,'1','MAGIC',0), -- approx
(93,'Dragon''s Roar',4,1,400,'HP','-(70+3*lv+(20*iq+3*str+10*mwep+100)*ar*k)','70+170*k','0','0','16','-(70+3*lv+(20*iq+3*str+10*mwep+100)*ar*k)','ATTACK,COMPUTE_MAGIC_DAMAGE,SPLASH,FIRE_CONT,FIRE',0,'NONE','lv+iq*3*k','(100+iq*5*k)/10',0,'','0','0','70+170*k',1,0,0,0,0,'1','MAGIC',0), -- approx
(94,'Blessing',4,1,0,'RESIST_NORMAL','((iq*0.3+5)*(2*k+0.5)+(dex*0.3))/(k+2.3)','50+100*k','600','0','3','((iq*0.3+5)*(2*k+0.5)+(dex*0.3))/(k+2.3)','TOGGLE',@AFF_HOSIN,'NONE','0','0',0,'','0','0','50+100*k',1,0,0,0,0,'1','NORMAL',0),
(95,'Reflect',4,1,0,'REFLECT_MELEE','5+(iq*0.2+str*0.1)*k','60+120*k','600','0','3','5+(iq*0.2+str*0.1)*k','TOGGLE',@AFF_BOHO,'NONE','0','0',0,'','0','0','60+120*k',1,0,0,0,0,'1','NORMAL',0),
(96,'Dragon''s Aid',4,1,0,'CRITICAL','(iq*0.3+5)*(2*k)/(k+3)','60+120*k','600','0','3','(iq*0.3+5)*(2*k)/(k+3)','TOGGLE',@AFF_GICHEON,'NONE','0','0',0,'','0','0','60+120*k',1,0,0,0,0,'1','NORMAL',0),
(106,'Lightning Throw',4,1,250,'HP','-(60+5*lv+(8*iq+2*dex+8*mwep+iq*number(5,15))*ar*k)','50+120*k','0','0','8','-(60+5*lv+(8*iq+2*dex+8*mwep+iq*number(5,15))*ar*k)','ATTACK,COMPUTE_MAGIC_DAMAGE,SPLASH,ELEC',0,'NONE','0','0',0,'','0','0','50+120*k',1,0,0,0,0,'1','MAGIC',0),
(107,'Summon Lightning',4,1,250,'HP','-(40+4*lv+(13*iq+2*str+10*mwep+iq*number(5,16))*ar*k)','60+150*k','0','0','12','-(40+4*lv+(13*iq+2*str+10*mwep+iq*number(5,16))*ar*k)','ATTACK,COMPUTE_MAGIC_DAMAGE,SPLASH,STUN,ELEC',0,'NONE','(30+70*2*k)/10','2',0,'','0','0','60+150*k',1,0,0,0,0,'1','MAGIC',0),
(108,'Lightning Claw',4,1,0,'HP','-((50+5*lv+(8*iq+2*str+8*mwep+number(1,800))*ar*k)*(1-0.1*chain))','70+170*k','0','0','14','-((50+5*lv+(8*iq+2*str+8*mwep+number(1,800))*ar*k)*(1-0.1*chain))','ATTACK,COMPUTE_MAGIC_DAMAGE,SLOW,ELEC',0,'NONE','(80+iq*5*k)/10','8',0,'','0','0','70+170*k',1,0,0,0,0,'1','MAGIC',0), -- approx
(109,'Cure',4,1,0,'HP','150+5*lv+(10*iq+6*mwep+number(600,800))*(k*0.15)','70+160*k','0','0','8','150+5*lv+(10*iq+6*mwep+number(600,800))*(k*0.15)','REMOVE_BAD_AFFECT',0,'NONE','20+80*k','0',0,'','0','0','70+160*k',1,0,0,0,0,'1','NORMAL',0),
(110,'Swiftness',4,1,0,'MOV_SPEED','(dex*0.2)+35*k','50+100*k','600','0','3','(dex*0.2)+35*k','TOGGLE',@AFF_KWAESOK,'CASTING_SPEED','3+33*k','600',0,'','0','0','50+100*k',1,0,0,0,0,'1','NORMAL',0),
(111,'Attack Up',4,1,0,'ATT_GRADE','3+(iq*0.2+str*0.1+11)*k','50+100*k','600','0','3','3+(iq*0.2+str*0.1+11)*k','TOGGLE',@AFF_JEUNGRYEOK,'NONE','0','0',0,'','0','0','50+100*k',1,0,0,0,0,'1','NORMAL',0),
(112,'Anti Dash',6,1,0,'NONE','24*k','0','0','0','0','24*k','',0,'NONE','0','0',0,'','0','0','0',1,0,0,0,0,'1','NORMAL',0), -- approx
(113,'Anti Ambush',6,1,0,'NONE','24*k','0','0','0','0','24*k','',0,'NONE','0','0',0,'','0','0','0',1,0,0,0,0,'1','NORMAL',0), -- approx
(114,'Anti Finger Strike',6,1,0,'NONE','24*k','0','0','0','0','24*k','',0,'NONE','0','0',0,'','0','0','0',1,0,0,0,0,'1','NORMAL',0), -- approx
(115,'Anti Shooting Dragon',6,1,0,'NONE','24*k','0','0','0','0','24*k','',0,'NONE','0','0',0,'','0','0','0',1,0,0,0,0,'1','NORMAL',0), -- approx
(116,'Anti Spirit Strike (W)',6,1,0,'NONE','24*k','0','0','0','0','24*k','',0,'NONE','0','0',0,'','0','0','0',1,0,0,0,0,'1','NORMAL',0), -- approx
(117,'Anti Repetitive Shot',6,1,0,'NONE','24*k','0','0','0','0','24*k','',0,'NONE','0','0',0,'','0','0','0',1,0,0,0,0,'1','NORMAL',0), -- approx
(118,'Anti Dark Orb',6,1,0,'NONE','24*k','0','0','0','0','24*k','',0,'NONE','0','0',0,'','0','0','0',1,0,0,0,0,'1','NORMAL',0), -- approx
(119,'Anti Summon Lightning',6,1,0,'NONE','24*k','0','0','0','0','24*k','',0,'NONE','0','0',0,'','0','0','0',1,0,0,0,0,'1','NORMAL',0), -- approx
(121,'Leadership',0,40,0,'NONE','0','0','0','0','0','0','',0,'NONE','0','0',0,'','0','0','0',1,20,0,0,0,'1','NORMAL',0),
(122,'Combo',0,2,0,'NONE','0','0','0','0','0','0','',0,'NONE','0','0',0,'','0','0','0',1,30,0,0,0,'1','NORMAL',0),
(123,'Fishing',0,40,0,'NONE','0','0','0','0','0','0','',0,'NONE','0','0',0,'','0','0','0',1,0,0,0,0,'1','NORMAL',0),
(124,'Mining',0,40,0,'NONE','0','0','0','0','0','0','',0,'NONE','0','0',0,'','0','0','0',1,0,0,0,0,'1','NORMAL',0),
(125,'Item Creation',0,40,0,'NONE','0','0','0','0','0','0','',0,'NONE','0','0',0,'','0','0','0',1,0,0,0,0,'1','NORMAL',0),
(126,'Shinsoo Language',0,20,0,'NONE','0','0','0','0','0','0','',0,'NONE','0','0',0,'','0','0','0',1,0,0,0,0,'1','NORMAL',0),
(127,'Chunjo Language',0,20,0,'NONE','0','0','0','0','0','0','',0,'NONE','0','0',0,'','0','0','0',1,0,0,0,0,'1','NORMAL',0),
(128,'Jinno Language',0,20,0,'NONE','0','0','0','0','0','0','',0,'NONE','0','0',0,'','0','0','0',1,0,0,0,0,'1','NORMAL',0),
(129,'Polymorph',0,40,0,'NONE','0','0','0','0','0','0','',0,'NONE','0','0',0,'','0','0','0',1,0,0,0,0,'1','NORMAL',0),
(130,'Horse Riding',0,40,0,'NONE','0','0','0','0','0','0','',0,'NONE','0','0',0,'','0','0','0',1,0,0,0,0,'1','NORMAL',0),
(131,'Call Horse',0,20,0,'NONE','0','0','0','0','0','0','',0,'NONE','0','0',0,'','0','0','0',1,0,0,0,0,'1','NORMAL',0),
(137,'Horseback Slash',5,1,250,'HP','-(atk+(0.5*atk+2*str+lv*2)*k)','30+80*k','0','0','5','-(atk+(0.5*atk+2*str+lv*2)*k)','ATTACK,USE_MELEE_DAMAGE,SPLASH,CRUSH',0,'NONE','0','0',0,'','0','0','30+80*k',1,0,0,0,0,'1','MELEE',0), -- approx
(138,'Horse Stump',5,1,250,'HP','-(1.5*atk+(0.6*atk+2*str+lv*2)*k)','40+100*k','0','0','10','-(1.5*atk+(0.6*atk+2*str+lv*2)*k)','ATTACK,USE_MELEE_DAMAGE,SPLASH,CRUSH',0,'MOV_SPEED','0','5',0,'','0','0','40+100*k',1,0,0,0,0,'1','MELEE',0), -- approx
(139,'Power Wave',5,1,500,'HP','-(2*atk+(0.8*atk+3*str+lv*2)*k)','50+120*k','0','0','12','-(2*atk+(0.8*atk+3*str+lv*2)*k)','ATTACK,USE_MELEE_DAMAGE,SELFONLY,SPLASH',0,'NONE','0','0',0,'','0','0','50+120*k',1,0,0,0,0,'1','MELEE',0), -- approx
(140,'Arrow Storm',5,1,400,'HP','-(atk+(0.5*atk+dex*3+lv*2)*k)','40+100*k','0','0','5','-(atk+(0.5*atk+dex*3+lv*2)*k)','ATTACK,SPLASH,USE_ARROW_DAMAGE',0,'NONE','0','0',0,'','0','0','40+100*k',1,0,0,0,0,'1','RANGE',0), -- approx
(141,'Regeneration Will',0,40,0,'NONE','k*1333.33','0','0','0','0','k*1333.33','',0,'NONE','0','0',0,'','0','0','0',1,0,0,0,0,'1','NORMAL',0),
(142,'Penetration Resist',0,40,0,'NONE','k*15','0','0','0','0','k*15','',0,'NONE','0','0',0,'','0','0','0',1,0,0,0,0,'1','NORMAL',0),
(144,'Monster Resist',0,40,0,'NONE','k*20','0','0','0','0','k*20','',0,'NONE','0','0',0,'','0','0','0',1,0,0,0,0,'1','NORMAL',0), -- approx
(151,'Dragon Eyes',0,7,0,'NONE','k*1400','0','0','0','0','k*1400','',0,'NONE','0','0',0,'','0','0','0',1,0,0,0,0,'1','NORMAL',0),
(152,'Blood of Dragon God',0,7,0,'MAX_HP','maxhp*k*0.2','150+350*k','600','0','1200','maxhp*k*0.2','',0,'NONE','0','0',0,'','0','0','150+350*k',1,0,0,0,0,'1','NORMAL',0), -- approx
(153,'Benediction of Dragon God',0,7,0,'MAX_SP','maxsp*k*0.2','150+350*k','600','0','1200','maxsp*k*0.2','',0,'NONE','0','0',0,'','0','0','150+350*k',1,0,0,0,0,'1','NORMAL',0), -- approx
(154,'Holy Armour',0,7,0,'DEF_GRADE','def*k*0.1','200+300*k','600','0','1200','def*k*0.1','',0,'NONE','0','0',0,'','0','0','200+300*k',1,0,0,0,0,'1','NORMAL',0), -- approx
(155,'Acceleration',0,7,0,'ATT_SPEED','k*15','250+350*k','600','0','1200','k*15','',0,'MOV_SPEED','k*15','600',0,'','0','0','250+350*k',1,0,0,0,0,'1','NORMAL',0), -- approx
(156,'Wrath of the Dragon God',0,7,0,'CRITICAL','k*50','300+500*k','600','0','1200','k*50','',0,'NONE','0','0',0,'','0','0','300+500*k',1,0,0,0,0,'1','NORMAL',0), -- approx
(157,'Casting Aid',0,7,0,'CASTING_SPEED','k*50','200+300*k','600','0','1200','k*50','',0,'NONE','0','0',0,'','0','0','200+300*k',1,0,0,0,0,'1','NORMAL',0), -- approx
(158,'Guild Teleport',0,7,0,'NONE','0','200+300*k','0','0','300','0','',0,'NONE','0','0',0,'','0','0','200+300*k',1,0,0,0,0,'1','NORMAL',0), -- approx
(159,'Guild Door',0,7,0,'NONE','0','200+300*k','0','0','300','0','',0,'NONE','0','0',0,'','0','0','200+300*k',1,0,0,0,0,'1','NORMAL',0), -- approx
(176,'Earthquake',1,1,400,'HP','-(3*atk+(0.9*atk+mwep+number(1,1000)+str*5+dex*3+lv)*k)','100+250*k','0','0','30','-(3*atk+(0.9*atk+mwep+number(1,1000)+str*5+dex*3+lv)*k)','ATTACK,USE_MELEE_DAMAGE,SPLASH',0,'NONE','0.4*k+(32*k/2)','0',0,'','0','0','100+250*k',1,0,0,0,0,'1','MELEE',0), -- approx
(177,'Light Stars',2,1,300,'HP','-(atk+(1.7*atk+mwep+number(1,1000)+dex*6+lv*5)*k)','100+250*k','0','0','30','-(atk+(1.7*atk+mwep+number(1,1000)+dex*6+lv*5)*k)','ATTACK,USE_MELEE_DAMAGE,SPLASH',0,'NONE','0.4*k+(32*k/2)','0',0,'','0','0','100+250*k',1,0,0,0,0,'1','RANGE',0), -- approx
(178,'Storm Shot',2,1,300,'HP','-(1.9*atk+(2.6*atk+mwep+number(1,1000))*k)','100+250*k','0','0','30','-(1.9*atk+(2.6*atk+mwep+number(1,1000))*k)','ATTACK,SPLASH,USE_ARROW_DAMAGE',0,'NONE','0.4*k+(32*k/2)','0',0,'','0','0','100+250*k',1,0,0,0,0,'1','RANGE',0), -- approx
(179,'Hell Strike',3,1,300,'HP','-(1.9*atk+(2.6*atk+mwep+number(1,1000))*k)','100+250*k','0','0','30','-(1.9*atk+(2.6*atk+mwep+number(1,1000))*k)','ATTACK,USE_MELEE_DAMAGE,SPLASH',0,'NONE','0.4*k+(32*k/2)','0',0,'','0','0','100+250*k',1,0,0,0,0,'1','MELEE',0), -- approx
(180,'Death Wave',3,1,400,'HP','-(120+6*lv+(5*con+5*dex+30*iq+number(1,1000)+9*mwep)*ar*k)','100+250*k','0','0','30','-(120+6*lv+(5*con+5*dex+30*iq+number(1,1000)+9*mwep)*ar*k)','ATTACK,COMPUTE_MAGIC_DAMAGE,SPLASH',0,'NONE','0.4*k+(32*k/2)','0',0,'','0','0','100+250*k',1,0,0,0,0,'1','MAGIC',0), -- approx
(181,'Meteor',4,1,400,'HP','-(120+6*lv+(5*con+5*dex+30*iq+number(1,1000)+9*mwep)*ar*k)','100+250*k','0','0','40','-(120+6*lv+(5*con+5*dex+30*iq+number(1,1000)+9*mwep)*ar*k)','ATTACK,COMPUTE_MAGIC_DAMAGE,SPLASH,FIRE_CONT,FIRE',0,'NONE','lv+iq*3*k','20*k',0,'','0','0','100+250*k',1,0,0,0,0,'1','MAGIC',0), -- approx
(182,'Aether Shield',4,1,0,'NONE','0.4*k+(18*k)','80+200*k','300','0','60','0.4*k+(18*k)','',@AFF_CHEONUN,'NONE','4*k','0',0,'','0','0','80+200*k',1,0,0,0,0,'1','NORMAL',0), -- approx
(256,'Monster Skill 256',0,1,300,'HP','-(2*lv+mwep*(1.2+k))','0','0','0','10','-(2*lv+mwep*(1.2+k))','ATTACK,SPLASH',0,'NONE','0','0',0,'','0','0','0',1,0,0,0,0,'1','MELEE',0), -- approx
(257,'Monster Skill 257',0,1,300,'HP','-(2*lv+mwep*(1.2+k))','0','0','0','10','-(2*lv+mwep*(1.2+k))','ATTACK,SPLASH',0,'NONE','0','0',0,'','0','0','0',1,0,0,0,0,'1','MELEE',0), -- approx
(258,'Monster Skill 258',0,1,300,'HP','-(2*lv+mwep*(1.2+k))','0','0','0','10','-(2*lv+mwep*(1.2+k))','ATTACK,SPLASH',0,'NONE','0','0',0,'','0','0','0',1,0,0,0,0,'1','MELEE',0), -- approx
(259,'Monster Skill 259',0,1,300,'HP','-(2*lv+mwep*(1.2+k))','0','0','0','10','-(2*lv+mwep*(1.2+k))','ATTACK,SPLASH',0,'NONE','0','0',0,'','0','0','0',1,0,0,0,0,'1','MELEE',0), -- approx
(260,'Monster Skill 260',0,1,300,'HP','-(2*lv+mwep*(1.2+k))','0','0','0','10','-(2*lv+mwep*(1.2+k))','ATTACK,SPLASH',0,'NONE','0','0',0,'','0','0','0',1,0,0,0,0,'1','MELEE',0), -- approx
(261,'Monster Skill 261',0,1,300,'HP','-(2*lv+mwep*(1.2+k))','0','0','0','10','-(2*lv+mwep*(1.2+k))','ATTACK,SPLASH,POISON',0,'NONE','30+30*k','0',0,'','0','0','0',1,0,0,0,0,'1','MELEE',0), -- approx
(265,'Ochao Healing',0,1,0,'NONE','0','0','0','0','15','0','PARTY',0,'NONE','0','0',0,'','0','0','0',1,0,0,0,0,'1','NORMAL',0); -- approx
