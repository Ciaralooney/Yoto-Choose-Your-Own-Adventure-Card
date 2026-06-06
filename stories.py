"""
Story bank for Yoto Jungle Adventure.

Each story is a tree of nodes. Every node has:
  - text: the narration played at this point
  - left: text describing the left choice
  - right: text describing the right choice
  - left_node / right_node: the key of the next node
  - OR ending: True (leaf node, story ends here)
  - ending_type: "triumph" | "mishap" | "surprise"
    (used to pick the right tone for the ending music cue)

Nodes are keyed as strings. Root is always "1".
A tree with 5 decision points has nodes at depths 1–5,
with 16 leaf (ending) nodes.

For readability each story is written as a flat dict.
Keys follow a binary path: "1" → "1L"/"1R" → "1LL"/"1LR"/"1RL"/"1RR" etc.
"""

STORIES = [
    # STORY 1: The Lost Baby Elephant
    {
        "title": "The Lost Baby Elephant",
        "intro": (
            "Deep in the heart of the jungle, you are a young explorer following "
            "a muddy trail when you hear a small, sad trumpeting sound. "
            "Pushing through the giant ferns, you find a tiny baby elephant "
            "sitting alone, its big eyes full of tears."
        ),
        "nodes": {
            "1": {
                "text": (
                    "The baby elephant looks up at you hopefully. "
                    "You need to help it find its herd! "
                    "You spot two trails leading away through the trees. "
                    "Fresh elephant tracks lead left toward the river, "
                    "but you can also hear distant rumbling to the right, deeper in the jungle."
                ),
                "left": "Follow the tracks to the river",
                "right": "Head toward the rumbling sound",
                "left_node": "1L",
                "right_node": "1R",
            },

            # ── LEFT BRANCH: River path ──────────────────────────────
            "1L": {
                "text": (
                    "You and the baby elephant follow the tracks through soft mud. "
                    "The river glitters through the trees ahead. "
                    "But at the water's edge, the tracks split. "
                    "Some lead upstream where colourful birds are calling, "
                    "others go downstream toward a wide sandbar where you can see large shapes moving."
                ),
                "left": "Go upstream toward the birds",
                "right": "Head downstream to the sandbar",
                "left_node": "1LL",
                "right_node": "1LR",
            },
            "1LL": {
                "text": (
                    "The birds lead you to a hidden waterfall. "
                    "Behind the falling water is a dark cave. "
                    "The baby elephant sniffs the air excitedly. "
                    "You could explore inside the cave, "
                    "or wait by the waterfall and listen carefully."
                ),
                "left": "Explore inside the cave",
                "right": "Wait and listen by the waterfall",
                "left_node": "1LLL",
                "right_node": "1LLR",
            },
            "1LLL": {
                "text": (
                    "Inside the cave you discover ancient carvings of elephants on the walls "
                    "and a tunnel leading deeper. "
                    "The baby elephant tugs your sleeve with its trunk. "
                    "Do you follow the tunnel, or head back outside?"
                ),
                "left": "Follow the tunnel",
                "right": "Head back outside",
                "left_node": "1LLLL",
                "right_node": "1LLLR",
            },
            "1LLLL": {
                "text": (
                    "The tunnel opens into a sunlit valley and there is the whole elephant herd, "
                    "splashing in a hidden pool! The baby elephant charges toward its mother "
                    "with joyful trumpeting. The mother wraps her trunk around you gently in thanks. "
                    "You found the most secret place in the entire jungle."
                ),
                "ending": True,
                "ending_type": "triumph",
            },
            "1LLLR": {
                "text": (
                    "Back outside, a wise old parrot lands on your shoulder. "
                    "In a scratchy voice it says: 'Herd… herd… east of the big fig tree!' "
                    "You follow its directions and sure enough, there is the herd waiting anxiously. "
                    "The baby elephant is home safe!"
                ),
                "ending": True,
                "ending_type": "triumph",
            },
            "1LLR": {
                "text": (
                    "You sit quietly by the waterfall. After a few minutes, "
                    "a family of otters appears and to your amazement, "
                    "they seem to understand your problem. "
                    "They dive and resurface, leading you along the river. "
                    "Do you trust them and follow, or find your own way?"
                ),
                "left": "Follow the otters",
                "right": "Find your own way",
                "left_node": "1LLRL",
                "right_node": "1LLRR",
            },
            "1LLRL": {
                "text": (
                    "The otters lead you straight to a shallow crossing where the elephant herd "
                    "is drinking on the other side! The baby wades across and is scooped up "
                    "by its mother's trunk. The otters chitter happily and splash back into the river. "
                    "What a team!"
                ),
                "ending": True,
                "ending_type": "triumph",
            },
            "1LLRR": {
                "text": (
                    "You try to navigate alone but end up going in circles. "
                    "As darkness falls you make camp under a giant tree. "
                    "In the morning the herd finds YOU they were searching all night! "
                    "A happy reunion, if a slightly backwards one."
                ),
                "ending": True,
                "ending_type": "mishap",
            },
            "1LR": {
                "text": (
                    "The sandbar is dotted with the enormous footprints of a whole herd! "
                    "But the herd has moved on. "
                    "A crocodile is sunbathing in the shallows, blocking the path. "
                    "You could try to sneak past very quietly, "
                    "or wade through the shallows on the other side."
                ),
                "left": "Sneak past the crocodile",
                "right": "Wade through the far shallows",
                "left_node": "1LRL",
                "right_node": "1LRR",
            },
            "1LRL": {
                "text": (
                    "You tiptoe so carefully that even the baby elephant holds its breath. "
                    "The crocodile snoozes on. "
                    "Beyond the sandbar you climb a tall hill and spot the herd below in a valley. "
                    "You slide down and reunite the baby with its trumpeting, delighted family!"
                ),
                "ending": True,
                "ending_type": "triumph",
            },
            "1LRR": {
                "text": (
                    "The shallows are deeper than they look! "
                    "You end up soaking wet and the baby elephant thinks this is hilarious, "
                    "splashing around joyfully. A passing ranger hears the commotion, "
                    "laughs at the sight of you, and radios the herd's location. "
                    "Reunited and very soggy."
                ),
                "ending": True,
                "ending_type": "mishap",
            },

            # ── RIGHT BRANCH: Deep jungle rumbling ───────────────────
            "1R": {
                "text": (
                    "You push through thick jungle toward the deep rumbling. "
                    "It gets louder and then stops. "
                    "You emerge into a clearing with a giant old baobab tree in the centre. "
                    "You could climb the tree to look for the herd from above, "
                    "or search around the roots, where something seems to be hiding."
                ),
                "left": "Climb the baobab tree",
                "right": "Search around the roots",
                "left_node": "1RL",
                "right_node": "1RR",
            },
            "1RL": {
                "text": (
                    "Halfway up the tree you can see for miles. "
                    "To the north, a cloud of red dust a moving herd! "
                    "To the south, smoke from a ranger station. "
                    "Which way do you head?"
                ),
                "left": "Head north toward the dust cloud",
                "right": "Head south to the ranger station",
                "left_node": "1RLL",
                "right_node": "1RLR",
            },
            "1RLL": {
                "text": (
                    "You run north through the trees. "
                    "The dust cloud is enormous dozens of elephants! "
                    "But they are moving fast. "
                    "Do you call out to them, or find a way to get ahead of the herd?"
                ),
                "left": "Call out loudly",
                "right": "Race ahead of the herd",
                "left_node": "1RLLL",
                "right_node": "1RLLR",
            },
            "1RLLL": {
                "text": (
                    "You shout as loud as you can. The herd slows. "
                    "An enormous matriarch turns and studies you carefully. "
                    "Then she sees the baby and lets out a thunderous trumpet call. "
                    "The whole herd gathers around the little one in a joyful huddle. "
                    "You did it!"
                ),
                "ending": True,
                "ending_type": "triumph",
            },
            "1RLLR": {
                "text": (
                    "You sprint through the undergrowth and manage to get ahead. "
                    "Standing in the path of the herd is terrifying but it works. "
                    "The lead elephant stops and sniffs the baby. "
                    "Recognition! The herd encircles the little elephant and rumbles softly. "
                    "A brave move that paid off."
                ),
                "ending": True,
                "ending_type": "triumph",
            },
            "1RLR": {
                "text": (
                    "The ranger station is run by a cheerful woman named Maya "
                    "who immediately knows which herd the baby belongs to. "
                    "She drives you out in her jeep. "
                    "But the jeep gets a flat tyre halfway there. "
                    "Do you wait for help, or walk the rest of the way?"
                ),
                "left": "Wait for help",
                "right": "Walk the rest of the way",
                "left_node": "1RLRL",
                "right_node": "1RLRR",
            },
            "1RLRL": {
                "text": (
                    "Another ranger arrives quickly and fixes the tyre. "
                    "You reach the herd just before sunset. "
                    "The baby elephant splashes into a muddy waterhole to celebrate, "
                    "covering you in mud. Worth it entirely."
                ),
                "ending": True,
                "ending_type": "triumph",
            },
            "1RLRR": {
                "text": (
                    "Walking through the jungle at dusk is spooky but magical. "
                    "You arrive just as the herd is settling for the night. "
                    "The reunion is quiet and tender the mother and baby sleep "
                    "curled together under the stars. You sleep nearby, content."
                ),
                "ending": True,
                "ending_type": "triumph",
            },
            "1RR": {
                "text": (
                    "Behind the giant roots you find a small monkey "
                    "who immediately steals your hat and climbs the baobab! "
                    "The baby elephant laughs. "
                    "The monkey seems to want you to follow it. "
                    "Do you chase the monkey up the tree, or ignore it and press on?"
                ),
                "left": "Chase the monkey up the tree",
                "right": "Ignore the monkey and press on",
                "left_node": "1RRL",
                "right_node": "1RRR",
            },
            "1RRL": {
                "text": (
                    "The monkey leads you through the treetops! "
                    "It's like a highway up here. "
                    "Below you can see the jungle clearly. "
                    "The monkey stops and points and there below is the elephant herd, "
                    "right beneath you. It drops your hat back on your head and vanishes. "
                    "Cheeky but helpful."
                ),
                "ending": True,
                "ending_type": "surprise",
            },
            "1RRR": {
                "text": (
                    "You press on through increasingly thick jungle. "
                    "The baby elephant uses its trunk to push branches aside for you "
                    "it is surprisingly good at this. "
                    "Eventually you both stumble out of the trees onto a wide plain, "
                    "and there is the herd, not fifty metres away. "
                    "Sometimes the direct route works!"
                ),
                "ending": True,
                "ending_type": "triumph",
            },
        },
    },
    
    # STORY 2: The Stolen River Stone
    {
        "title": "The Stolen River Stone",
        "intro": (
            "You are paddling a wooden canoe down a slow jungle river "
            "when a flash of light catches your eye. On a rock in the middle of the river "
            "sits a glowing green stone but as you reach for it, "
            "a cheeky river otter snatches it and dives beneath the surface!"
        ),
        "nodes": {
            "1": {
                "text": (
                    "The otter pops up downstream, the glowing stone in its mouth, "
                    "watching you with bright eyes. "
                    "You could dive in and try to swim after it, "
                    "or paddle your canoe as fast as you can to cut it off."
                ),
                "left": "Dive in and swim after it",
                "right": "Paddle the canoe to cut it off",
                "left_node": "1L",
                "right_node": "1R",
            },

            "1L": {
                "text": (
                    "The water is cool and clear. The otter is fast but playful "
                    "it keeps looking back at you as if this is a game. "
                    "It ducks under a waterlogged tree. "
                    "You could squeeze under too, or swim around the log."
                ),
                "left": "Squeeze under the log",
                "right": "Swim around the log",
                "left_node": "1LL",
                "right_node": "1LR",
            },
            "1LL": {
                "text": (
                    "Under the log is a whole hidden world submerged tree roots "
                    "twinkling with tiny fish. The otter waits for you on a muddy bank ahead. "
                    "It drops the stone and sniffs your hand curiously. "
                    "Maybe it just wanted to play! "
                    "But now you notice the stone is cracked. "
                    "Do you take it anyway, or leave it for the river?"
                ),
                "left": "Take the cracked stone",
                "right": "Leave it for the river",
                "left_node": "1LLL",
                "right_node": "1LLR",
            },
            "1LLL": {
                "text": (
                    "You carry the stone home. That night it glows green on your windowsill "
                    "and the crack slowly heals itself. "
                    "In the morning it hums with a warm light. "
                    "Do you keep it, or return to the river to put it back?"
                ),
                "left": "Keep it",
                "right": "Return it to the river",
                "left_node": "1LLLL",
                "right_node": "1LLLR",
            },
            "1LLLL": {
                "text": (
                    "The stone sits on your shelf for years, glowing softly, "
                    "and every time you feel lost or sad it seems to shine a little brighter. "
                    "You never find out what it truly is, but some magic is best left mysterious."
                ),
                "ending": True,
                "ending_type": "surprise",
            },
            "1LLLR": {
                "text": (
                    "You return the stone to the exact rock where you found it. "
                    "The moment it touches the rock the whole river shimmers green for a second. "
                    "The otter appears and bows its head. "
                    "You get the feeling you did something important even if you don't know what."
                ),
                "ending": True,
                "ending_type": "triumph",
            },
            "1LLR": {
                "text": (
                    "You leave the stone on the muddy bank. "
                    "A large heron lands, picks it up carefully, and flies upriver. "
                    "The otter watches it go, satisfied, then leads you to an island "
                    "covered in the most beautiful flowers you have ever seen. "
                    "Your reward, perhaps."
                ),
                "ending": True,
                "ending_type": "surprise",
            },
            "1LR": {
                "text": (
                    "Swimming around the log you spot an underwater cave. "
                    "Through the entrance you can see the glow of the stone inside. "
                    "You could swim into the cave, or surface and look for another way in."
                ),
                "left": "Swim into the cave",
                "right": "Surface and find another way",
                "left_node": "1LRL",
                "right_node": "1LRR",
            },
            "1LRL": {
                "text": (
                    "The cave opens into an air pocket a secret chamber! "
                    "The stone sits on a natural shelf, glowing steadily. "
                    "The otter is there too, watching you. "
                    "It picks up the stone and places it gently in your hands. "
                    "It was guarding it for you all along."
                ),
                "ending": True,
                "ending_type": "surprise",
            },
            "1LRR": {
                "text": (
                    "You find a root bridge above the cave entrance, climb down, "
                    "and retrieve the stone from a shallow ledge just inside. "
                    "Easy! But as you swim back, a rainbow appears over the river "
                    "even though it isn't raining. Some things in the jungle defy explanation."
                ),
                "ending": True,
                "ending_type": "surprise",
            },

            "1R": {
                "text": (
                    "You paddle furiously and get ahead of the otter. "
                    "It surfaces right beside your canoe, stone in mouth, "
                    "looking impressed. It drops the stone into the canoe and dives away. "
                    "Just like that! But now the stone is warm in your hands and pulsing. "
                    "You notice it is pointing like a compass. "
                    "Do you follow where it points, or paddle back to camp?"
                ),
                "left": "Follow where the stone points",
                "right": "Paddle back to camp",
                "left_node": "1RL",
                "right_node": "1RR",
            },
            "1RL": {
                "text": (
                    "The stone leads you around a bend to a part of the river "
                    "you have never seen before. A stone archway covered in moss "
                    "rises out of the water. "
                    "Do you paddle through the archway, or circle around it?"
                ),
                "left": "Paddle through the archway",
                "right": "Circle around it",
                "left_node": "1RLL",
                "right_node": "1RLR",
            },
            "1RLL": {
                "text": (
                    "Through the archway the jungle transforms "
                    "the trees are taller, the colours more vivid, the air sparkling. "
                    "Animals gather at the water's edge watching you. "
                    "The stone stops glowing. "
                    "Do you step ashore into this magical place, or turn back?"
                ),
                "left": "Step ashore",
                "right": "Turn back",
                "left_node": "1RLLL",
                "right_node": "1RLLR",
            },
            "1RLLL": {
                "text": (
                    "You spend what feels like an afternoon in the most beautiful place "
                    "you have ever seen. When you paddle home the stone is dark and cold "
                    "its magic used up. But the memory stays with you forever."
                ),
                "ending": True,
                "ending_type": "triumph",
            },
            "1RLLR": {
                "text": (
                    "You turn back through the archway. "
                    "When you glance behind you, the archway is gone just river. "
                    "The stone in your hand turns to ordinary pebble. "
                    "But you know what you saw."
                ),
                "ending": True,
                "ending_type": "surprise",
            },
            "1RLR": {
                "text": (
                    "Circling the archway, the stone goes cold. "
                    "A fish leaps out of the water and snatches it from your hands! "
                    "It disappears with a splash. "
                    "The otter surfaces nearby, shrugs (otters can definitely shrug), "
                    "and swims away. Some adventures end mysteriously."
                ),
                "ending": True,
                "ending_type": "mishap",
            },
            "1RR": {
                "text": (
                    "Back at camp the stone sits quietly in your tent. "
                    "That night you dream of the otter showing you an underground river "
                    "full of glowing stones. "
                    "In the morning the stone is gone but so are your muddy boots, "
                    "replaced with clean ones. "
                    "Do you go back to search for the otter, or accept the mystery?"
                ),
                "left": "Go back to find the otter",
                "right": "Accept the mystery",
                "left_node": "1RRL",
                "right_node": "1RRR",
            },
            "1RRL": {
                "text": (
                    "You spend three days searching but never find the otter again. "
                    "On the last day a green light pulses once from deep in the river, "
                    "and you feel certain it is a goodbye. "
                    "Some friends are only meant to cross your path once."
                ),
                "ending": True,
                "ending_type": "surprise",
            },
            "1RRR": {
                "text": (
                    "You accept it. Clean boots, strange dreams, a story nobody will believe. "
                    "That evening a letter arrives at camp addressed to you "
                    "in handwriting that looks like paw prints. "
                    "It says simply: 'Thank you.' "
                    "You still have no idea what any of it meant. Perfect."
                ),
                "ending": True,
                "ending_type": "surprise",
            },
        },
    },
    
    # STORY 3: The Night the Jungle Went Dark
    {
        "title": "The Night the Jungle Went Dark",
        "intro": (
            "You are a young jungle ranger on your first solo night watch "
            "when every single light goes out at once the camp lanterns, the torches, "
            "even the fireflies. Total darkness. "
            "Then, from somewhere nearby, you hear a very small voice say: "
            "'Hello? Is someone there? I need help.'"
        ),
        "nodes": {
            "1": {
                "text": (
                    "The voice is coming from ground level something small. "
                    "You fumble for your matches. "
                    "By the tiny flame you see a young slow loris sitting in the path, "
                    "its enormous eyes reflecting your match. "
                    "'The light-keeper has gone missing,' it says seriously. "
                    "'Without her the jungle stays dark all night.' "
                    "You could follow the loris immediately, "
                    "or go back to camp for supplies first."
                ),
                "left": "Follow the loris immediately",
                "right": "Go back to camp for supplies",
                "left_node": "1L",
                "right_node": "1R",
            },

            "1L": {
                "text": (
                    "The loris moves surprisingly fast. "
                    "It leads you to a grove of enormous mushrooms that glow faintly"
                    "just enough to see by. "
                    "In the centre of the grove is a hole in the ground, "
                    "and from it comes a soft crying sound. "
                    "Do you climb down into the hole, or call into it first?"
                ),
                "left": "Climb down",
                "right": "Call into it first",
                "left_node": "1LL",
                "right_node": "1LR",
            },
            "1LL": {
                "text": (
                    "You climb down into a cosy underground chamber. "
                    "Sitting in the corner is the light-keeper"
                    "a tiny firefly queen, her wings tangled in a spider's web. "
                    "She is so relieved to see you. "
                    "Do you carefully untangle her wings yourself, "
                    "or ask the loris to help with its nimble fingers?"
                ),
                "left": "Untangle her yourself",
                "right": "Ask the loris to help",
                "left_node": "1LLL",
                "right_node": "1LLR",
            },
            "1LLL": {
                "text": (
                    "Your fingers are clumsy at first but you work patiently and slowly. "
                    "The last thread comes free. "
                    "The firefly queen rises into the air and blazes like a tiny sun. "
                    "Outside, millions of fireflies answer her call, "
                    "and the jungle erupts in golden light. "
                    "You did it all by yourself."
                ),
                "ending": True,
                "ending_type": "triumph",
            },
            "1LLR": {
                "text": (
                    "The loris works with extraordinary delicacy, "
                    "humming to itself as it unpicks each thread. "
                    "The queen is free in moments. She rises up blazing with light "
                    "and the whole jungle lights up in response. "
                    "You couldn't have done it without a friend."
                ),
                "ending": True,
                "ending_type": "triumph",
            },
            "1LR": {
                "text": (
                    "You call down: 'Hello? Are you alright?' "
                    "A tiny voice calls back: 'My wings are stuck! I can't get out!' "
                    "The loris tugs your sleeve: 'She needs something to grab onto.' "
                    "Do you lower your scarf into the hole, or find a long stick?"
                ),
                "left": "Lower your scarf",
                "right": "Find a long stick",
                "left_node": "1LRL",
                "right_node": "1LRR",
            },
            "1LRL": {
                "text": (
                    "The firefly queen grabs your scarf and you haul her up gently. "
                    "In the open air her wings dry and she shakes herself free. "
                    "She rises up and calls her swarm. "
                    "The jungle floods with warm light and the loris claps its tiny hands. "
                    "Your scarf now glows faintly, forever after."
                ),
                "ending": True,
                "ending_type": "triumph",
            },
            "1LRR": {
                "text": (
                    "You find a stick but it snaps when the queen grabs it, "
                    "and she falls back down with an indignant squeak. "
                    "You end up climbing down after all. "
                    "You untangle her wings and she zooms up out of the hole. "
                    "The jungle lights up in seconds. "
                    "A slight detour, but still a success!"
                ),
                "ending": True,
                "ending_type": "mishap",
            },

            "1R": {
                "text": (
                    "Back at camp you grab a torch, rope, and some food just in case. "
                    "Smart thinking! When you return, the loris is impatiently tapping its foot. "
                    "It leads you to a vast dark lake you never knew was there. "
                    "A boat is tied at the edge. "
                    "Do you take the boat across the lake, or walk around the shore?"
                ),
                "left": "Take the boat across",
                "right": "Walk around the shore",
                "left_node": "1RL",
                "right_node": "1RR",
            },
            "1RL": {
                "text": (
                    "The lake is perfectly still and black as ink. "
                    "In the middle your torch picks out a tiny island"
                    "and on it, a glass jar with something glowing inside. "
                    "Do you row straight for the jar, or circle the island cautiously first?"
                ),
                "left": "Row straight for the jar",
                "right": "Circle the island first",
                "left_node": "1RLL",
                "right_node": "1RLR",
            },
            "1RLL": {
                "text": (
                    "You grab the jar. Inside, the firefly queen is curled up asleep"
                    "someone trapped her here. You open the lid and she wakes with a start, "
                    "then rockets into the sky blazing bright. "
                    "The whole lake lights up. Every firefly in the jungle answers. "
                    "You row back through the most beautiful light show you've ever seen."
                ),
                "ending": True,
                "ending_type": "triumph",
            },
            "1RLR": {
                "text": (
                    "Circling the island you spot that it isn't real"
                    "it's a floating mass of leaves with the jar on top. "
                    "You almost missed it! You fish it out with your rope, "
                    "open the jar, and the firefly queen soars free. "
                    "The jungle blazes back to life around you. "
                    "Caution paid off."
                ),
                "ending": True,
                "ending_type": "triumph",
            },
            "1RR": {
                "text": (
                    "The shore path is longer but you discover a trail of glowing paw prints "
                    "leading into the trees. "
                    "The loris sees them too and whispers: 'The thief went this way.' "
                    "Do you follow the paw prints, or stick to the shore?"
                ),
                "left": "Follow the paw prints",
                "right": "Stick to the shore",
                "left_node": "1RRL",
                "right_node": "1RRR",
            },
            "1RRL": {
                "text": (
                    "The paw prints lead to a pangolin, curled up asleep, "
                    "with the firefly queen trapped in its scales she rolled in by accident! "
                    "You gently uncurl the pangolin. "
                    "The queen tumbles free, stretches her wings, and blazes alight. "
                    "The pangolin snores through the whole thing."
                ),
                "ending": True,
                "ending_type": "surprise",
            },
            "1RRR": {
                "text": (
                    "You stick to the shore and eventually find a small beach "
                    "where the firefly queen is sitting in a rock pool, wings soaking wet. "
                    "She just fell in! Nothing sinister at all. "
                    "You dry her wings carefully with your scarf. "
                    "She lights up, takes off, and the jungle follows. "
                    "Not every mystery has a villain."
                ),
                "ending": True,
                "ending_type": "surprise",
            },
        },
    },

]
