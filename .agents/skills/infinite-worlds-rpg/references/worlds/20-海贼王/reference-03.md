> 本包角色数据快照：2026-09-19。支持文档；其中历史对照值不替代levels.md。游戏权限与Rank44以上公设统一服从[核心规则](../../core-rules.md)。

# 海贼王 逐行依据

## P00 普通海兵／未强化船员

Rank0（人体系数1）。普通人员没有因所属海军或海贼自动获得建筑级强招；普通体能的行政军官也适用此行。

来源：[P1 ONE PIECE 官方剧情总索引](https://one-piece.com/story/index.html)。

## 军衔拆分的共同依据

中文上尉、少校、中校、上校分别对应原作日文大尉、少佐、中佐、大佐；准尉在少尉以下，准将在上校与少将之间。[军衔索引](https://onepiece.fandom.com/wiki/Marine_Ranks)用于核对分类；官方人物页可核对[贝鲁梅伯的少佐](https://one-piece.com/character/Helmeppo/index.html)、[云雀的中佐](https://one-piece.com/character/Hibari/index.html)及[老鼠的支部大佐](https://one-piece.com/character/Nezumi/index.html)。这些资料证明军衔及人物身份，不提供固定能量倍率。

本次按用户确认的具体军衔拆行。原PC1、PC2退为历史分组ID，新行各有确定采用值，但证据均为D。曲线参数见[世界与计算](reference-01.md)；工程插值不是新增原著战绩，人物也不因晋升自动获得表中倍数。

## PC0 海军准尉

**采用Rank0（人体系数2），证据D。** P00的普通人体参照为1，本行采用受训者代表系数2，区分阶内体能水平。项目已有[受训人体采用2的例子](../22-一拳超人/levels.md)，此处复用其工程参数形式，不以另一作品人物的战绩证明海军准尉实力。

系数2是本次选用的相对体能工作值，原著没有给出“准尉恰为普通人两倍”的统一数据；它也不是焦耳或自结合能倍率。Rank0保留为受训人体代表的D类采用，未证明所有准尉均低于Rank1；出现具体物质作用证据时依实际表现改判。旧说明把“缺少独立物质目标锚”当成归入普通人体的理由，并省略阶内参数，现撤销该推断：缺证不能证明与普通人相同。

## PC1a 海军少尉

**采用Rank1（1倍），U = 3.706 × 10⁻⁹ J，证据D。** 采用项目现有砖块参照，作为细分曲线的低端工程假设。原著没有“取得少尉军衔即可整体毁砖”的统一规定；此起点不是作者给定的能力门槛。

## PC1b 海军中尉

**采用Rank1+（4.394倍），U = 1.628 × 10⁻⁸ J，证据D。** 位于少尉与上尉两工程参照之间；按序号k=2取分段对数插值。没有把中尉军衔或一次败绩直接换成焦耳数。

## PC1c 海军上尉

**采用Rank1+（19.30倍），U = 7.154 × 10⁻⁸ J，证据D。** 沿用此前尉官分组的木构件代表值。旧依据中[芬布迪](https://one-piece.com/character/Fullbody/index.html)在巴拉蒂时期的身份是大尉，故本次将该代表点保留于上尉，而非挪到中尉。

模型为1.5 m × 0.8 m × 0.04 m、密度600 kg/m³的木构件，质量28.8 kg，用项目长方体自引力积分计算。上述尺寸与整件处理情景仍是工程假设，未从原作分镜测得；官方页记载的败于山治也不是其破坏上限证明。

## PC2a 海军少校

**采用Rank1+（390.2倍），U = 1.446 × 10⁻⁶ J，证据D。** 按序号k=4，在上尉与上校两工程参照之间取曲线值。[贝鲁梅伯官方页](https://one-piece.com/character/Helmeppo/index.html)只用于确认少佐即本表少校，不把其全部个人经历当成少校统一出力。

## PC2b 海军中校

**采用Rank1+（7886倍），U = 2.923 × 10⁻⁵ J，证据D。** 按序号k=5，在上尉与上校段取曲线值。[云雀官方页](https://one-piece.com/character/Hibari/index.html)可核对中佐身份及狙击专长，不能据军衔推出固定破坏量，也未用于量定本行数值。

## PC2c 海军上校

**采用Rank2（1倍），U = 5.907 × 10⁻⁴ J，证据D。** 沿用此前校官分组的墙板代表值。旧依据中的[蒙卡](https://one-piece.com/character/Morgan/index.html)、[老鼠](https://one-piece.com/character/Nezumi/index.html)为支部上校背景，不能当作全体本部上校的同强度证明；本次仅保留既有D参照，不按本部／支部另拆新行。

模型为既定3 m × 3 m × 0.2 m、密度2400 kg/m³墙板，质量4320 kg。原著没有量定此参数。老鼠败于早期娜美不能反算其精确上限，也不能证明校官普遍等于本值。

## PC2d 海军准将

**采用Rank2+（20.81万倍），U = 1.229 × 10² J，证据D。** 补入上校与少将之间的正式军衔，按序号k=7取曲线值。其高端使用旧PC3少将估值，因此继承旧锚的不确定性，不能当作准将已有独立物质战绩的证明；若后续校正少将锚，本行须随之重算。

## PC3 海军将官·少将战斗模板

Rank3+（12.49万倍）。海军将官能力不均，作为中段普通战斗模板。 q=4 是工程配置，非称号固有量。

来源：[P1 ONE PIECE 官方剧情总索引](https://one-piece.com/story/index.html)；[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P7 ONE PIECE 官方蛋头岛剧情](https://one-piece.com/story/egghead/index.html)；[P8 ONE PIECE 官方凯多人物页](https://one-piece.com/character/Kaido/index.html)；[P9 ONE PIECE 官方King人物页](https://one-piece.com/character/King/index.html)。本行是所述配置的一次强作用工程采用点，不是该身份全体成员的保证下限或原著全力上限。

## PC4 海军中将·普通战斗模板

Rank4+（2.67倍）。卡普等特例须另用顶层模板；“中将”不能保证人人同档。 q=6 是工程配置，非称号固有量。

来源：[P1 ONE PIECE 官方剧情总索引](https://one-piece.com/story/index.html)；[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P7 ONE PIECE 官方蛋头岛剧情](https://one-piece.com/story/egghead/index.html)；[P8 ONE PIECE 官方凯多人物页](https://one-piece.com/character/Kaido/index.html)；[P9 ONE PIECE 官方King人物页](https://one-piece.com/character/King/index.html)。本行是所述配置的一次强作用工程采用点，不是该身份全体成员的保证下限或原著全力上限。

## PC5 海军大将·成熟战斗模板

Rank4+（1.774万倍）。与四皇处同一顶层竞争区，能力克制和时代会影响结果。 q=9 是工程配置，非称号固有量。

来源：[P1 ONE PIECE 官方剧情总索引](https://one-piece.com/story/index.html)；[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P7 ONE PIECE 官方蛋头岛剧情](https://one-piece.com/story/egghead/index.html)；[P8 ONE PIECE 官方凯多人物页](https://one-piece.com/character/Kaido/index.html)；[P9 ONE PIECE 官方King人物页](https://one-piece.com/character/King/index.html)。本行是所述配置的一次强作用工程采用点，不是该身份全体成员的保证下限或原著全力上限。

## PC6 海军元帅·顶层战斗模板

Rank4+（1.774万倍）。任职变化不证明战力立刻增长；与大将同物理预算是身份不增幅。 q=9 是工程配置，非称号固有量。

来源：[P1 ONE PIECE 官方剧情总索引](https://one-piece.com/story/index.html)；[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P7 ONE PIECE 官方蛋头岛剧情](https://one-piece.com/story/egghead/index.html)；[P8 ONE PIECE 官方凯多人物页](https://one-piece.com/character/Kaido/index.html)；[P9 ONE PIECE 官方King人物页](https://one-piece.com/character/King/index.html)。本行是所述配置的一次强作用工程采用点，不是该身份全体成员的保证下限或原著全力上限。

## PC7 东海强敌／低赏金·条件模板

Rank3（1倍）。地区和赏金不能直接反推每个人实力；以东海主要战斗敌人作为采用样本。 q=0 是工程配置，非称号固有量。

来源：[P1 ONE PIECE 官方剧情总索引](https://one-piece.com/story/index.html)；[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P7 ONE PIECE 官方蛋头岛剧情](https://one-piece.com/story/egghead/index.html)；[P8 ONE PIECE 官方凯多人物页](https://one-piece.com/character/Kaido/index.html)；[P9 ONE PIECE 官方King人物页](https://one-piece.com/character/King/index.html)。本行是所述配置的一次强作用工程采用点，不是该身份全体成员的保证下限或原著全力上限。

## PC8 伟大航路前半强敌·条件模板

Rank3+（6644倍）。赏金低于一亿不是本值必要条件，也不是充分条件。 q=3 是工程配置，非称号固有量。

来源：[P1 ONE PIECE 官方剧情总索引](https://one-piece.com/story/index.html)；[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P7 ONE PIECE 官方蛋头岛剧情](https://one-piece.com/story/egghead/index.html)；[P8 ONE PIECE 官方凯多人物页](https://one-piece.com/character/Kaido/index.html)；[P9 ONE PIECE 官方King人物页](https://one-piece.com/character/King/index.html)。本行是所述配置的一次强作用工程采用点，不是该身份全体成员的保证下限或原著全力上限。

## PC9 超新星·首次登场战斗型模板

Rank3+（234.8万倍）。同称号只表悬赏及时代；不是任一时期超新星都锁本值。 q=5 是工程配置，非称号固有量。

来源：[P1 ONE PIECE 官方剧情总索引](https://one-piece.com/story/index.html)；[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P7 ONE PIECE 官方蛋头岛剧情](https://one-piece.com/story/egghead/index.html)；[P8 ONE PIECE 官方凯多人物页](https://one-piece.com/character/Kaido/index.html)；[P9 ONE PIECE 官方King人物页](https://one-piece.com/character/King/index.html)。本行是所述配置的一次强作用工程采用点，不是该身份全体成员的保证下限或原著全力上限。

## PC10 王下七武海·战斗型中位配置

Rank4+（2.67倍）。巴基、鹰眼等差异极大；七武海为政治制度，绝不能普遍套此中位。 q=6 是工程配置，非称号固有量。

来源：[P1 ONE PIECE 官方剧情总索引](https://one-piece.com/story/index.html)；[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P7 ONE PIECE 官方蛋头岛剧情](https://one-piece.com/story/egghead/index.html)；[P8 ONE PIECE 官方凯多人物页](https://one-piece.com/character/Kaido/index.html)；[P9 ONE PIECE 官方King人物页](https://one-piece.com/character/King/index.html)。本行是所述配置的一次强作用工程采用点，不是该身份全体成员的保证下限或原著全力上限。

## PC11 四皇干部·普通战斗配置

Rank4+（11.58倍）。干部非统一军衔，多种梯队；此处指成熟作战而非杂兵。 q=6.5 是工程配置，非称号固有量。

来源：[P1 ONE PIECE 官方剧情总索引](https://one-piece.com/story/index.html)；[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P7 ONE PIECE 官方蛋头岛剧情](https://one-piece.com/story/egghead/index.html)；[P8 ONE PIECE 官方凯多人物页](https://one-piece.com/character/Kaido/index.html)；[P9 ONE PIECE 官方King人物页](https://one-piece.com/character/King/index.html)。本行是所述配置的一次强作用工程采用点，不是该身份全体成员的保证下限或原著全力上限。

## PC12 皇团最高干部·完整战斗配置

Rank4+（217.7倍）。最高干部含不同专长，不能据“皇副”非正式称谓统一。 q=7.5 是工程配置，非称号固有量。

来源：[P1 ONE PIECE 官方剧情总索引](https://one-piece.com/story/index.html)；[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P7 ONE PIECE 官方蛋头岛剧情](https://one-piece.com/story/egghead/index.html)；[P8 ONE PIECE 官方凯多人物页](https://one-piece.com/character/Kaido/index.html)；[P9 ONE PIECE 官方King人物页](https://one-piece.com/character/King/index.html)。本行是所述配置的一次强作用工程采用点，不是该身份全体成员的保证下限或原著全力上限。

## PC13 四皇·成熟直接战斗模板

Rank4+（1.774万倍）。排除巴基误认式战力归类；政治头衔本身不赋予本值。 q=9 是工程配置，非称号固有量。

来源：[P1 ONE PIECE 官方剧情总索引](https://one-piece.com/story/index.html)；[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P7 ONE PIECE 官方蛋头岛剧情](https://one-piece.com/story/egghead/index.html)；[P8 ONE PIECE 官方凯多人物页](https://one-piece.com/character/Kaido/index.html)；[P9 ONE PIECE 官方King人物页](https://one-piece.com/character/King/index.html)。本行是所述配置的一次强作用工程采用点，不是该身份全体成员的保证下限或原著全力上限。

## PC14 海贼王时代顶尖对抗·战斗模板

Rank4+（7.693万倍）。以罗杰/巅峰白胡子/卡普的对抗层而非称号自动升级；半单位是统一曲线关系估计。 q=9.5 是工程配置，非称号固有量。

来源：[P1 ONE PIECE 官方剧情总索引](https://one-piece.com/story/index.html)；[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P7 ONE PIECE 官方蛋头岛剧情](https://one-piece.com/story/egghead/index.html)；[P8 ONE PIECE 官方凯多人物页](https://one-piece.com/character/Kaido/index.html)；[P9 ONE PIECE 官方King人物页](https://one-piece.com/character/King/index.html)。本行是所述配置的一次强作用工程采用点，不是该身份全体成员的保证下限或原著全力上限。

## PC15 五老星·已显现战斗体模板

Rank4+（1.774万倍）。再生与特殊能力单列；本值不是证明其能正面压过所有四皇。 q=9 是工程配置，非称号固有量。

来源：[P1 ONE PIECE 官方剧情总索引](https://one-piece.com/story/index.html)；[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P7 ONE PIECE 官方蛋头岛剧情](https://one-piece.com/story/egghead/index.html)；[P8 ONE PIECE 官方凯多人物页](https://one-piece.com/character/Kaido/index.html)；[P9 ONE PIECE 官方King人物页](https://one-piece.com/character/King/index.html)。本行是所述配置的一次强作用工程采用点，不是该身份全体成员的保证下限或原著全力上限。

## PG1 司法岛时期·常态成熟攻击

Rank3+（2.881万倍）。该时期身体基础；不是早期东海或和之国常态。；共享 q 模型。

来源：[P2 ONE PIECE 官方司法岛剧情](https://one-piece.com/story/enies_lobby/index.html)；[P3 ONE PIECE 官方：四档首次登场制作访谈](https://one-piece.com/usop/o20160127_0511/index.html)；[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P5 ONE PIECE 官方第1072集／原作第103卷](https://one-piece.com/anime/62948/index.html)；[P6 ONE PIECE 官方第1076集／原作第104卷](https://one-piece.com/anime/63846/index.html)；[P10 ONE PIECE 官方海贼无双4路飞资料](https://oppw4-20.bn-ent.net/character/luffy/)。时代、基础素质与霸气已包含于本行，禁止再乘另一个霸气表数值。

## PG2 司法岛时期·二档

Rank3+（12.49万倍）。同一时期速度/连打强化，官方未给全属性倍数。；共享 q 模型。

来源：[P2 ONE PIECE 官方司法岛剧情](https://one-piece.com/story/enies_lobby/index.html)；[P3 ONE PIECE 官方：四档首次登场制作访谈](https://one-piece.com/usop/o20160127_0511/index.html)；[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P5 ONE PIECE 官方第1072集／原作第103卷](https://one-piece.com/anime/62948/index.html)；[P6 ONE PIECE 官方第1076集／原作第104卷](https://one-piece.com/anime/63846/index.html)；[P10 ONE PIECE 官方海贼无双4路飞资料](https://oppw4-20.bn-ent.net/character/luffy/)。时代、基础素质与霸气已包含于本行，禁止再乘另一个霸气表数值。

## PG3 司法岛时期·三档单击

Rank3+（54.16万倍）。巨人肢体的重攻击，速度损失不能抹去；只比较单次重击预算。；共享 q 模型。

来源：[P2 ONE PIECE 官方司法岛剧情](https://one-piece.com/story/enies_lobby/index.html)；[P3 ONE PIECE 官方：四档首次登场制作访谈](https://one-piece.com/usop/o20160127_0511/index.html)；[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P5 ONE PIECE 官方第1072集／原作第103卷](https://one-piece.com/anime/62948/index.html)；[P6 ONE PIECE 官方第1076集／原作第104卷](https://one-piece.com/anime/63846/index.html)；[P10 ONE PIECE 官方海贼无双4路飞资料](https://oppw4-20.bn-ent.net/character/luffy/)。时代、基础素质与霸气已包含于本行，禁止再乘另一个霸气表数值。

## PG4 修行后·常态＋基础霸气

Rank3+（234.8万倍）。两年修行后统一新底数；不能让所有时代常态同值。；共享 q 模型。

来源：[P2 ONE PIECE 官方司法岛剧情](https://one-piece.com/story/enies_lobby/index.html)；[P3 ONE PIECE 官方：四档首次登场制作访谈](https://one-piece.com/usop/o20160127_0511/index.html)；[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P5 ONE PIECE 官方第1072集／原作第103卷](https://one-piece.com/anime/62948/index.html)；[P6 ONE PIECE 官方第1076集／原作第104卷](https://one-piece.com/anime/63846/index.html)；[P10 ONE PIECE 官方海贼无双4路飞资料](https://oppw4-20.bn-ent.net/character/luffy/)。时代、基础素质与霸气已包含于本行，禁止再乘另一个霸气表数值。

## PG5 修行后·二档成熟配置

Rank3+（1018万倍）。基础成长后的二档，不将旧二档数值照搬。；共享 q 模型。

来源：[P2 ONE PIECE 官方司法岛剧情](https://one-piece.com/story/enies_lobby/index.html)；[P3 ONE PIECE 官方：四档首次登场制作访谈](https://one-piece.com/usop/o20160127_0511/index.html)；[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P5 ONE PIECE 官方第1072集／原作第103卷](https://one-piece.com/anime/62948/index.html)；[P6 ONE PIECE 官方第1076集／原作第104卷](https://one-piece.com/anime/63846/index.html)；[P10 ONE PIECE 官方海贼无双4路飞资料](https://oppw4-20.bn-ent.net/character/luffy/)。时代、基础素质与霸气已包含于本行，禁止再乘另一个霸气表数值。

## PG6 修行后·三档硬化重击

Rank4+（2.67倍）。硬化巨人肢体配置。；共享 q 模型。

来源：[P2 ONE PIECE 官方司法岛剧情](https://one-piece.com/story/enies_lobby/index.html)；[P3 ONE PIECE 官方：四档首次登场制作访谈](https://one-piece.com/usop/o20160127_0511/index.html)；[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P5 ONE PIECE 官方第1072集／原作第103卷](https://one-piece.com/anime/62948/index.html)；[P6 ONE PIECE 官方第1076集／原作第104卷](https://one-piece.com/anime/63846/index.html)；[P10 ONE PIECE 官方海贼无双4路飞资料](https://oppw4-20.bn-ent.net/character/luffy/)。时代、基础素质与霸气已包含于本行，禁止再乘另一个霸气表数值。

## PG7 四档·弹跳人（德岛成熟配置）

Rank4+（50.2倍）。四档的弹性/霸气结合，实际能压制明哥但有时限。；共享 q 模型。

来源：[P2 ONE PIECE 官方司法岛剧情](https://one-piece.com/story/enies_lobby/index.html)；[P3 ONE PIECE 官方：四档首次登场制作访谈](https://one-piece.com/usop/o20160127_0511/index.html)；[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P5 ONE PIECE 官方第1072集／原作第103卷](https://one-piece.com/anime/62948/index.html)；[P6 ONE PIECE 官方第1076集／原作第104卷](https://one-piece.com/anime/63846/index.html)；[P10 ONE PIECE 官方海贼无双4路飞资料](https://oppw4-20.bn-ent.net/character/luffy/)。时代、基础素质与霸气已包含于本行，禁止再乘另一个霸气表数值。

## PG8 四档·坦克人（满腹条件）

Rank4+（50.2倍）。防御/反弹取向，并非比弹跳人更高一级；物理预算同值，额外饱食条件保留。；共享 q 模型。

来源：[P2 ONE PIECE 官方司法岛剧情](https://one-piece.com/story/enies_lobby/index.html)；[P3 ONE PIECE 官方：四档首次登场制作访谈](https://one-piece.com/usop/o20160127_0511/index.html)；[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P5 ONE PIECE 官方第1072集／原作第103卷](https://one-piece.com/anime/62948/index.html)；[P6 ONE PIECE 官方第1076集／原作第104卷](https://one-piece.com/anime/63846/index.html)；[P10 ONE PIECE 官方海贼无双4路飞资料](https://oppw4-20.bn-ent.net/character/luffy/)。时代、基础素质与霸气已包含于本行，禁止再乘另一个霸气表数值。

## PG9 四档·蛇人（蛋糕岛配置）

Rank4+（50.2倍）。追踪和速度取向，不能用击败同一个敌人的剧情把所有单击强度强制抬级。；共享 q 模型。

来源：[P2 ONE PIECE 官方司法岛剧情](https://one-piece.com/story/enies_lobby/index.html)；[P3 ONE PIECE 官方：四档首次登场制作访谈](https://one-piece.com/usop/o20160127_0511/index.html)；[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P5 ONE PIECE 官方第1072集／原作第103卷](https://one-piece.com/anime/62948/index.html)；[P6 ONE PIECE 官方第1076集／原作第104卷](https://one-piece.com/anime/63846/index.html)；[P10 ONE PIECE 官方海贼无双4路飞资料](https://oppw4-20.bn-ent.net/character/luffy/)。时代、基础素质与霸气已包含于本行，禁止再乘另一个霸气表数值。

## PG10 和之国·高级武装色四档

Rank4+（943.8倍）。内破/放出训练后的完整配置，不只改招式命名。；共享 q 模型。

来源：[P2 ONE PIECE 官方司法岛剧情](https://one-piece.com/story/enies_lobby/index.html)；[P3 ONE PIECE 官方：四档首次登场制作访谈](https://one-piece.com/usop/o20160127_0511/index.html)；[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P5 ONE PIECE 官方第1072集／原作第103卷](https://one-piece.com/anime/62948/index.html)；[P6 ONE PIECE 官方第1076集／原作第104卷](https://one-piece.com/anime/63846/index.html)；[P10 ONE PIECE 官方海贼无双4路飞资料](https://oppw4-20.bn-ent.net/character/luffy/)。时代、基础素质与霸气已包含于本行，禁止再乘另一个霸气表数值。

## PG11 和之国·霸王色缠绕主战配置

Rank4+（4092倍）。可以直接进入凯多顶层对抗，但连续败战/消耗仍存在。；共享 q 模型。

来源：[P2 ONE PIECE 官方司法岛剧情](https://one-piece.com/story/enies_lobby/index.html)；[P3 ONE PIECE 官方：四档首次登场制作访谈](https://one-piece.com/usop/o20160127_0511/index.html)；[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P5 ONE PIECE 官方第1072集／原作第103卷](https://one-piece.com/anime/62948/index.html)；[P6 ONE PIECE 官方第1076集／原作第104卷](https://one-piece.com/anime/63846/index.html)；[P10 ONE PIECE 官方海贼无双4路飞资料](https://oppw4-20.bn-ent.net/character/luffy/)。时代、基础素质与霸气已包含于本行，禁止再乘另一个霸气表数值。

## PG12 五档／尼卡觉醒·主战配置

Rank4+（1.774万倍）。身体与环境的弹性化、自由战斗；不是无限想象力或任意现实改写。；共享 q 模型。

来源：[P2 ONE PIECE 官方司法岛剧情](https://one-piece.com/story/enies_lobby/index.html)；[P3 ONE PIECE 官方：四档首次登场制作访谈](https://one-piece.com/usop/o20160127_0511/index.html)；[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P5 ONE PIECE 官方第1072集／原作第103卷](https://one-piece.com/anime/62948/index.html)；[P6 ONE PIECE 官方第1076集／原作第104卷](https://one-piece.com/anime/63846/index.html)；[P10 ONE PIECE 官方海贼无双4路飞资料](https://oppw4-20.bn-ent.net/character/luffy/)。时代、基础素质与霸气已包含于本行，禁止再乘另一个霸气表数值。

## PG13 五档·猿神枪终结配置

Rank5+（3.336倍）。巨型终结重击单列，需准备、巨大化与霸气。D=20 km区域是工程情景，不是拳头官方直径。；共享 q 模型。

来源：[P2 ONE PIECE 官方司法岛剧情](https://one-piece.com/story/enies_lobby/index.html)；[P3 ONE PIECE 官方：四档首次登场制作访谈](https://one-piece.com/usop/o20160127_0511/index.html)；[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P5 ONE PIECE 官方第1072集／原作第103卷](https://one-piece.com/anime/62948/index.html)；[P6 ONE PIECE 官方第1076集／原作第104卷](https://one-piece.com/anime/63846/index.html)；[P10 ONE PIECE 官方海贼无双4路飞资料](https://oppw4-20.bn-ent.net/character/luffy/)。时代、基础素质与霸气已包含于本行，禁止再乘另一个霸气表数值。

## PH1 见闻色·基本感知（统一身体底数）

Rank4+（2.67倍）。非直接能量技能，提升探测/预警。；同一身体底数测试配置，不与路飞整态相乘。

来源：[P1 ONE PIECE 官方剧情总索引](https://one-piece.com/story/index.html)；[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P7 ONE PIECE 官方蛋头岛剧情](https://one-piece.com/story/egghead/index.html)。本行是所述配置的一次强作用工程采用点，不是该身份全体成员的保证下限或原著全力上限。 本行U只记录固定测试者身体参照；感知、未来视、威压、位移等机制效果不接受此GBE评分，不能据此给实际使用者定值。

## PH2 见闻色·短期预见未来（同底数）

Rank4+（2.67倍）。未来视不自动增加物理出力；与基础见闻同值有明确量纲原因。；同一身体底数测试配置，不与路飞整态相乘。

来源：[P1 ONE PIECE 官方剧情总索引](https://one-piece.com/story/index.html)；[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P7 ONE PIECE 官方蛋头岛剧情](https://one-piece.com/story/egghead/index.html)。本行是所述配置的一次强作用工程采用点，不是该身份全体成员的保证下限或原著全力上限。 本行U只记录固定测试者身体参照；感知、未来视、威压、位移等机制效果不接受此GBE评分，不能据此给实际使用者定值。

## PH3 武装色·基础覆盖

Rank4+（2.67倍）。统一成熟身体底数 q=6。；同一身体底数测试配置，不与路飞整态相乘。

来源：[P1 ONE PIECE 官方剧情总索引](https://one-piece.com/story/index.html)；[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P7 ONE PIECE 官方蛋头岛剧情](https://one-piece.com/story/egghead/index.html)。本行是所述配置的一次强作用工程采用点，不是该身份全体成员的保证下限或原著全力上限。

## PH4 武装色·强化硬化

Rank4+（11.58倍）。覆层强化的工程半单位进度。；同一身体底数测试配置，不与路飞整态相乘。

来源：[P1 ONE PIECE 官方剧情总索引](https://one-piece.com/story/index.html)；[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P7 ONE PIECE 官方蛋头岛剧情](https://one-piece.com/story/egghead/index.html)。本行是所述配置的一次强作用工程采用点，不是该身份全体成员的保证下限或原著全力上限。

## PH5 武装色·外放

Rank4+（50.2倍）。外放而非接触，改变作用机制；半单位系工程非原作数值。；同一身体底数测试配置，不与路飞整态相乘。

来源：[P1 ONE PIECE 官方剧情总索引](https://one-piece.com/story/index.html)；[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P7 ONE PIECE 官方蛋头岛剧情](https://one-piece.com/story/egghead/index.html)。本行是所述配置的一次强作用工程采用点，不是该身份全体成员的保证下限或原著全力上限。

## PH6 武装色·内部破坏

Rank4+（217.7倍）。内部破坏可绕过外层防御，不等于把整个目标质量炸飞。；同一身体底数测试配置，不与路飞整态相乘。

来源：[P1 ONE PIECE 官方剧情总索引](https://one-piece.com/story/index.html)；[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P7 ONE PIECE 官方蛋头岛剧情](https://one-piece.com/story/egghead/index.html)。本行是所述配置的一次强作用工程采用点，不是该身份全体成员的保证下限或原著全力上限。

## PH7 霸王色·威压控制（同身体底数）

Rank4+（2.67倍）。主要是意志震慑；不把昏倒人数换成人体全部结合能。；同一身体底数测试配置，不与路飞整态相乘。

来源：[P1 ONE PIECE 官方剧情总索引](https://one-piece.com/story/index.html)；[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P7 ONE PIECE 官方蛋头岛剧情](https://one-piece.com/story/egghead/index.html)。本行是所述配置的一次强作用工程采用点，不是该身份全体成员的保证下限或原著全力上限。 本行U只记录固定测试者身体参照；感知、未来视、威压、位移等机制效果不接受此GBE评分，不能据此给实际使用者定值。

## PH8 霸王色·攻击缠绕模板

Rank4+（943.8倍）。以顶层战斗所需条件为关系锚；不是普通觉醒霸王色就达到此值。；同一身体底数测试配置，不与路飞整态相乘。

来源：[P1 ONE PIECE 官方剧情总索引](https://one-piece.com/story/index.html)；[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P7 ONE PIECE 官方蛋头岛剧情](https://one-piece.com/story/egghead/index.html)。本行是所述配置的一次强作用工程采用点，不是该身份全体成员的保证下限或原著全力上限。

## PF1 超人系·成熟能力运用模板

Rank3+（234.8万倍）。类型不是强度，同类能力差异很大。 未公开确认的自然系觉醒不擅造为既定境界。

来源：[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P5 ONE PIECE 官方第1072集／原作第103卷](https://one-piece.com/anime/62948/index.html)；[P8 ONE PIECE 官方凯多人物页](https://one-piece.com/character/Kaido/index.html)；[P9 ONE PIECE 官方King人物页](https://one-piece.com/character/King/index.html)。本行是所述配置的一次强作用工程采用点，不是该身份全体成员的保证下限或原著全力上限。

## PF2 超人系·觉醒运用模板

Rank4+（2.67倍）。环境/对象作用方式扩展；例外能力按个体覆盖模板。 未公开确认的自然系觉醒不擅造为既定境界。

来源：[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P5 ONE PIECE 官方第1072集／原作第103卷](https://one-piece.com/anime/62948/index.html)；[P8 ONE PIECE 官方凯多人物页](https://one-piece.com/character/Kaido/index.html)；[P9 ONE PIECE 官方King人物页](https://one-piece.com/character/King/index.html)。本行是所述配置的一次强作用工程采用点，不是该身份全体成员的保证下限或原著全力上限。

## PF3 自然系·成熟能力运用模板

Rank3+（234.8万倍）。元素化改变命中条件，不自带比超人系更高结合能。 未公开确认的自然系觉醒不擅造为既定境界。

来源：[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P5 ONE PIECE 官方第1072集／原作第103卷](https://one-piece.com/anime/62948/index.html)；[P8 ONE PIECE 官方凯多人物页](https://one-piece.com/character/Kaido/index.html)；[P9 ONE PIECE 官方King人物页](https://one-piece.com/character/King/index.html)。本行是所述配置的一次强作用工程采用点，不是该身份全体成员的保证下限或原著全力上限。

## PF4 动物系·人形基础模板

Rank3+（234.8万倍）。共同素质底数。 未公开确认的自然系觉醒不擅造为既定境界。

来源：[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P5 ONE PIECE 官方第1072集／原作第103卷](https://one-piece.com/anime/62948/index.html)；[P8 ONE PIECE 官方凯多人物页](https://one-piece.com/character/Kaido/index.html)；[P9 ONE PIECE 官方King人物页](https://one-piece.com/character/King/index.html)。本行是所述配置的一次强作用工程采用点，不是该身份全体成员的保证下限或原著全力上限。

## PF5 动物系·兽形战斗模板

Rank3+（1018万倍）。体型与特长变化；不是所有兽形都优于人兽形。 未公开确认的自然系觉醒不擅造为既定境界。

来源：[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P5 ONE PIECE 官方第1072集／原作第103卷](https://one-piece.com/anime/62948/index.html)；[P8 ONE PIECE 官方凯多人物页](https://one-piece.com/character/Kaido/index.html)；[P9 ONE PIECE 官方King人物页](https://one-piece.com/character/King/index.html)。本行是所述配置的一次强作用工程采用点，不是该身份全体成员的保证下限或原著全力上限。

## PF6 动物系·人兽形战斗模板

Rank3+（1018万倍）。与兽形相同物理预算，保留形态/技巧差异。 未公开确认的自然系觉醒不擅造为既定境界。

来源：[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P5 ONE PIECE 官方第1072集／原作第103卷](https://one-piece.com/anime/62948/index.html)；[P8 ONE PIECE 官方凯多人物页](https://one-piece.com/character/Kaido/index.html)；[P9 ONE PIECE 官方King人物页](https://one-piece.com/character/King/index.html)。本行是所述配置的一次强作用工程采用点，不是该身份全体成员的保证下限或原著全力上限。

## PF7 动物系·觉醒战斗模板

Rank4+（2.67倍）。觉醒后的恢复、体能与意志问题分开；不是无条件无损。 未公开确认的自然系觉醒不擅造为既定境界。

来源：[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P5 ONE PIECE 官方第1072集／原作第103卷](https://one-piece.com/anime/62948/index.html)；[P8 ONE PIECE 官方凯多人物页](https://one-piece.com/character/Kaido/index.html)；[P9 ONE PIECE 官方King人物页](https://one-piece.com/character/King/index.html)。本行是所述配置的一次强作用工程采用点，不是该身份全体成员的保证下限或原著全力上限。

## PF8 古代种·成熟模板

Rank4+（2.67倍）。古代种是种类，不是普通种必经升级；此行设高体格游戏模板。 未公开确认的自然系觉醒不擅造为既定境界。

来源：[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P5 ONE PIECE 官方第1072集／原作第103卷](https://one-piece.com/anime/62948/index.html)；[P8 ONE PIECE 官方凯多人物页](https://one-piece.com/character/Kaido/index.html)；[P9 ONE PIECE 官方King人物页](https://one-piece.com/character/King/index.html)。本行是所述配置的一次强作用工程采用点，不是该身份全体成员的保证下限或原著全力上限。

## PF9 幻兽种·成熟模板

Rank4+（2.67倍）。幻兽种各有额外机制，并非天然高于所有古代种；同值是模板而非物种定理。 未公开确认的自然系觉醒不擅造为既定境界。

来源：[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P5 ONE PIECE 官方第1072集／原作第103卷](https://one-piece.com/anime/62948/index.html)；[P8 ONE PIECE 官方凯多人物页](https://one-piece.com/character/Kaido/index.html)；[P9 ONE PIECE 官方King人物页](https://one-piece.com/character/King/index.html)。本行是所述配置的一次强作用工程采用点，不是该身份全体成员的保证下限或原著全力上限。

## PR1 六式·剃（统一精锐身体）

Rank3+（12.49万倍）。六式是技能集，并非六个递增境界；统一身体底数仅比较配置。此式主要改变位移，不伪造单独能量增幅。

来源：[P2 ONE PIECE 官方司法岛剧情](https://one-piece.com/story/enies_lobby/index.html)。独立技能，不可将六行相乘。这里的U是固定测试者身体参照，不是剃、月步或纸绘产生同等物质作用。 本行U只记录固定测试者身体参照；感知、未来视、威压、位移等机制效果不接受此GBE评分，不能据此给实际使用者定值。

## PR2 六式·月步（统一精锐身体）

Rank3+（12.49万倍）。六式是技能集，并非六个递增境界；统一身体底数仅比较配置。此式主要改变空中移动，不伪造单独能量增幅。

来源：[P2 ONE PIECE 官方司法岛剧情](https://one-piece.com/story/enies_lobby/index.html)。独立技能，不可将六行相乘。这里的U是固定测试者身体参照，不是剃、月步或纸绘产生同等物质作用。 本行U只记录固定测试者身体参照；感知、未来视、威压、位移等机制效果不接受此GBE评分，不能据此给实际使用者定值。

## PR3 六式·铁块（统一精锐身体）

Rank3+（12.49万倍）。六式是技能集，并非六个递增境界；统一身体底数仅比较配置。此式主要改变防御，不伪造单独能量增幅。

来源：[P2 ONE PIECE 官方司法岛剧情](https://one-piece.com/story/enies_lobby/index.html)。独立技能，不可将六行相乘。这里的U是固定测试者身体参照，不是剃、月步或纸绘产生同等物质作用。 本行U只记录固定测试者身体参照；感知、未来视、威压、位移等机制效果不接受此GBE评分，不能据此给实际使用者定值。

## PR4 六式·纸绘（统一精锐身体）

Rank3+（12.49万倍）。六式是技能集，并非六个递增境界；统一身体底数仅比较配置。此式主要改变闪避，不伪造单独能量增幅。

来源：[P2 ONE PIECE 官方司法岛剧情](https://one-piece.com/story/enies_lobby/index.html)。独立技能，不可将六行相乘。这里的U是固定测试者身体参照，不是剃、月步或纸绘产生同等物质作用。 本行U只记录固定测试者身体参照；感知、未来视、威压、位移等机制效果不接受此GBE评分，不能据此给实际使用者定值。

## PR5 六式·指枪（统一精锐身体）

Rank3+（12.49万倍）。六式是技能集，并非六个递增境界；统一身体底数仅比较配置。此式主要改变穿透，不伪造单独能量增幅。

来源：[P2 ONE PIECE 官方司法岛剧情](https://one-piece.com/story/enies_lobby/index.html)。独立技能，不可将六行相乘。这里的U是固定测试者身体参照，不是剃、月步或纸绘产生同等物质作用。 本行U只记录固定测试者身体参照；感知、未来视、威压、位移等机制效果不接受此GBE评分，不能据此给实际使用者定值。

## PR6 六式·岚脚（统一精锐身体）

Rank3+（12.49万倍）。六式是技能集，并非六个递增境界；统一身体底数仅比较配置。此式主要改变斩击，不伪造单独能量增幅。

来源：[P2 ONE PIECE 官方司法岛剧情](https://one-piece.com/story/enies_lobby/index.html)。独立技能，不可将六行相乘。这里的U是固定测试者身体参照，不是剃、月步或纸绘产生同等物质作用。 本行U只记录固定测试者身体参照；感知、未来视、威压、位移等机制效果不接受此GBE评分，不能据此给实际使用者定值。

## PR7 六式奥义·六王枪

Rank3+（54.16万倍）。以司法岛路奇的高阶综合技能定位，比普通单式高半个共同进度单位；倍率为工程估计，原文没有GBE数字。

来源：[P2 ONE PIECE 官方司法岛剧情](https://one-piece.com/story/enies_lobby/index.html)。本行是所述配置的一次强作用工程采用点，不是该身份全体成员的保证下限或原著全力上限。

## PO1 鬼岛终结攻击·20 km区域情景

Rank5+（3.336倍）。猿神枪/终战相关区域采用D=20 km、h=D/38的薄盘情景，尺寸非原文精确值；供共享曲线末端统一校准。

来源：[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)；[P6 ONE PIECE 官方第1076集／原作第104卷](https://one-piece.com/anime/63846/index.html)。本行是所述配置的一次强作用工程采用点，不是该身份全体成员的保证下限或原著全力上限。

## PO2 鲁鲁西亚毁灭·古代兵器一次作用情景

Rank5+（15.05万倍）。官方蛋头回顾确认母火供能的古代兵器毁国；采用直径100 km、厚度10 km区域作为缺尺寸条件代表。不能把“国家”直接默认日本国土，也不能将此写进伊姆身体值。

来源：[P7 ONE PIECE 官方蛋头岛剧情](https://one-piece.com/story/egghead/index.html)。本行是所述配置的一次强作用工程采用点，不是该身份全体成员的保证下限或原著全力上限。

## PO3 冥王·毁岛声明工程情景

Rank5+（3.336倍）。冥王是兵器而非境界；原作第193话等的毁岛定位，本次仅有官方篇章索引作章节导航。采用20 km区域的有限游戏模板，不是实际展示测量。

来源：[P1 ONE PIECE 官方剧情总索引](https://one-piece.com/story/index.html)；[P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)。本行是所述配置的一次强作用工程采用点，不是该身份全体成员的保证下限或原著全力上限。

## 来源索引

- [P1 ONE PIECE 官方剧情总索引](https://one-piece.com/story/index.html)：官方列漫画篇章话数：东海1—100、司法岛375—441、顶上550—597等。仅索引不视为读过所有分镜。
- [P2 ONE PIECE 官方司法岛剧情](https://one-piece.com/story/enies_lobby/index.html)：路飞二档击败布鲁诺、三档及二档与路奇决战，屠魔令是舰队炮击。官方全文已核。
- [P3 ONE PIECE 官方：四档首次登场制作访谈](https://one-piece.com/usop/o20160127_0511/index.html)：四档与猿王枪的正式称谓、明哥战；制作访谈不能提供漫画固定能量倍率。
- [P4 ONE PIECE 官方和之国剧情](https://one-piece.com/story/land_of_wano2/index.html)：四皇统治与四皇联盟、鬼岛讨伐的正式剧情结构；部分页段未给招式长度。
- [P5 ONE PIECE 官方第1072集／原作第103卷](https://one-piece.com/anime/62948/index.html)：五档弹性化环境、巨大化、体力消耗及恢复鼓点。动画介绍是漫画变身机制的官方旁证，不移植额外动画破坏量。
- [P6 ONE PIECE 官方第1076集／原作第104卷](https://one-piece.com/anime/63846/index.html)：猿神枪与凯多终战；本轮检索可读摘要，页面直读403，未声称取得原分镜测距。
- [P7 ONE PIECE 官方蛋头岛剧情](https://one-piece.com/story/egghead/index.html)：官方全文：母火是动力，失窃后古代兵器毁灭国家；古代战争长期沉陆；五老星战斗/再生；古代机器人释放储存的乔伊波伊霸气。不是伊姆本体一击。
- [P8 ONE PIECE 官方凯多人物页](https://one-piece.com/character/Kaido/index.html)：百兽海贼团、鱼鱼果实幻兽种青龙、悬赏金额。悬赏是身份数据，不是焦耳或严格实力函数。
- [P9 ONE PIECE 官方King人物页](https://one-piece.com/character/King/index.html)：大看板/古代种身份及悬赏，支持将皇团干部与果实类型分开。
- [P10 ONE PIECE 官方海贼无双4路飞资料](https://oppw4-20.bn-ent.net/character/luffy/)：官方授权游戏列二档速度、三档力量与四档弹跳人/蛇人。仅辅助译名/分支导航；游戏伤害数值不用于本表。
- [P11 ONE PIECE 官方：2026艾尔巴夫动画预告](https://www.youtube.com/watch?v=6HeXamLfppc)：官方频道说明2026年4月起艾尔巴夫篇。说明作品仍在延展；本表实质核算截止蛋头已完成段落，不声称最新连载全内容已核。

## 2026-09-19 入门复核

普通新兵 P00 的Rank0·H1与准尉 PC0 的Rank0·H2保留。前者指未有超常强化的新兵配置，后者是受训准尉的D代表，两个Rank0并不表示数值相同。[原作官方克比资料](https://one-piece.com/character/Coby/index.html)将入队、杂务训练、掌握剃与觉醒见闻色按经历分开；不能把后来的六式、霸气或英雄事迹回填入伍当天。军衔本身也不是统一肉体境界。

本轮复核没有改变少尉、中尉、上尉、少校、中校、上校等已拆开的军衔。PC0的2是工程参数，不是原文宣告准尉全员两倍；后续砖、木构件、墙板各点仍按原表D模型使用，不能因入口复核而把全军衔表说成已获原著定量证明。
