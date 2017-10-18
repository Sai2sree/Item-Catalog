from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Genre, Base, Book, User

engine = create_engine('sqlite:///genresofbookswithusers.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Amarendra Bahubali", email="amarendra@bahubali.com",
             picture='https://www.hdwallpapers.in/walls/prabhas_bahubali_part'
             '_2-wide.jpg')
session.add(User1)
session.commit()

# Science Fiction - Books
genre1 = Genre(user_id=1, name="Science Fiction")

session.add(genre1)
session.commit()

book1 = Book(user_id=1,
             picture="http://via.placeholder.com/400x500",
             name="The Stone Sky",
             author="N.K.Jemisin",
             description="""THIS IS THE WAY THE WORLD ENDS... FOR THE LAST TIME.
             The Moon will soon return.
             Whether this heralds the destruction of humankind or
             something worse will depend on two women.
             Essun has inherited the power of Alabaster Tenring.
             With it, she hopes to find her daughter Nassun and forge
             a world in which every orogene child can grow up safe.
             For Nassun, her mother's mastery of Obelisk Gate comes too late.
             She has seen the evil of the world, and accepted what her mother
             will not admit: that sometimes what is corrupt cannot be cleansed,
             only destroyed""",
             price="$2.99",
             rating="4.48/5",
             genre=genre1)

session.add(book1)
session.commit()

book2 = Book(user_id=1,
             picture="http://via.placeholder.com/400x500",
             name="The Hearts We Sold",
             author="Emily Lloyd-Jones",
             description="""When Dee Moreno makes a deal with a demon,
             that her heart in exchange for escape from disastrous home life.
             She finds the trade may have been more than she bargained for.
             And becoming 'heartless' is only the beginning.
             What lies ahead is a nightmare far bigger, far more monstrous
             than anything she could have ever imagined.
             With reality turned on its head, Dee has only a group of
             other deal making teens to keep her grounded,
             including the charming but secretive James Lancer.
             And as something grows between them amid an otherworldy ordeal,
             Dee begins to wonder whether she can give someone her heart when
             its no longer hers to give?""",
             price="$2.99",
             rating="3.94/5",
             genre=genre1)

session.add(book2)
session.commit()

book3 = Book(user_id=1,
             picture="http://via.placeholder.com/400x500",
             name="The Dazzling Heights",
             author="Katharine McGee",
             description="""New York City, 2118. Manhattan is home to a
             thousand story supertower, a breathtaking marvel that touches
             the sky. But amid high tech luxury and futuristic glamour,
             five teenagers are keeping dangerous secrets.
             Leda is haunted by memories of what happened on the worst night
             of her life. She will do anything to make sure the truth stays
             hidden even if it means trusting her enemy. Watt just wants to
             put everything behind him until Leda forces him to start
             hacking again. Will he do what it takes to be free of her
             for good?""",
             price="$2.99",
             rating="4.09/5",
             genre=genre1)

session.add(book3)
session.commit()


book4 = Book(user_id=1,
             picture="http://via.placeholder.com/400x500",
             name="Reincarnation Blues",
             author="Michael Poore",
             description="""What if you could live forever but without your
             one true love. Reincarnation Blues is the story of a man who
             has been reincarnated nearly 10,000 times, in search of the
             secret to immortality so that he can be with his beloved, the
             incarnation of Death. Neil Gaiman meets Kurt Vonnegut in this
             darkly whimsical, hilariously profound, and wildly imaginative
             comedy of the secrets of life and love. Transporting us
             from ancient India to outer space to Renaissance Italy to the
             present day, is a journey through time, space, and
             the human heart.""",
             price="$2.99",
             rating="4.06/5",
             genre=genre1)

session.add(book4)
session.commit()


# Romance - Books
genre2 = Genre(user_id=1, name="Romance")

session.add(genre2)
session.commit()

book1 = Book(user_id=1,
             picture="http://via.placeholder.com/400x500",
             name="Wicked Like a Wildfire",
             author="Lana Popovic",
             description="""All the women in Iris and Malina s family have
             the unique magical ability or 'gleam' to manipulate beauty.
             Iris sees flowers as fractals and turns her kaleidoscope
             visions into glasswork, while Malina interprets moods as music.
             But their mother has strict rules to keep their gifts a secret,
             even in their secluded sea-side town. Iris and Malina are not
             allowed to share their magic with anyone, and above all, they
             are forbidden from falling in love. But when their mother is
             mysteriously attacked, the sisters will have to unearth the
             truth behind the quiet lives their mother has built for them.
             They will discover a wicked curse that haunts their family line
             but will they find that the very magic that bonds them together
             is destined to tear them apart forever?""",
             price="$2.99",
             rating="3.7/5",
             genre=genre2)

session.add(book1)
session.commit()

book2 = Book(user_id=1,
             picture="http://via.placeholder.com/400x500",
             name="Royally Endowed",
             author="Emma Chase",
             description="""Logan St. James is a smoldering, sexy beast.
             Sure, he can be a little broody at times but Ellie Hammonds
             willing to overlook that. Because, have you seen him?? Sexy.
             As. Hell. And Ellie is perky enough for both of them.
             For years, she had a crush on the intense,
             gorgeous royal security guard but she does not think
             he ever saw her, not really.
             To Logan, Ellie was just part of the job, a relative of the
             royal family he had sworn to protect. Now, at 22 years old
             and fresh out of college, she is determined to put aside her
             X rated dreams of pat downs and pillow talk,
             and find a real life happily ever after.
             The Queen of Wessco encourages Ellie to follow in her sister
             footsteps and settle down with a prince of her own. Or a duke,
             a marqui a viscount would also do nicely.
             But in the pursuit of a fairy tale ending, Ellie learns that
             the sweetest crushes can be the hardest to let go.
             Logan St. James grew up on the wrong side of the tracks, in a
             family on the wrong side of the law. But these days, he
             covers his tattoos and scars with a respectable suit. He is
             handsome, loyal, brave, skilled with his hands
             and other body parts.
             Any woman would be proud to call him hers.
             But there is only one woman he wants.
             For years he has watched over her, protected her, held her
             hair back when she was sick, taught her how to throw a punch,
             and spot a liar. He dreams of her. Would lay down his life for
             her. But beautiful Ellie Hammonds off-limits.
             Everybody knows the bodyguard rules: Never lose focus,
             never let them out of your sight, and never, ever fall
             in love.""",
             price="$2.99",
             rating="4.25/5",
             genre=genre2)

session.add(book2)
session.commit()

book3 = Book(user_id=1,
             picture="http://via.placeholder.com/400x500",
             name="The Color Project",
             author="Sierra Abrams",
             description="""Bernice Aurora Wescott has one thing she doesn't want
             anyone to know: her name. That is, until Bee meets Levi,
             the local golden boy who runs a charity organization called The
             Color Project.
             Levi is not at all shy about attempting to guess Bee real name;
             his persistence is one of the many reasons why Bee falls for him.
             But while Levi is everything she never knew she needed, giving up
             her name would feel like a stamp on forever and that terrifies
             her. When unexpected news of an illness in the family drains
             Bee summer of everything bright, she is pushed to the
             breaking point. Losing herself in The Color Project, a world
             of weddings, funerals, cancer patients, and hopeful families
             that the charity funds is no longer enough. Bee must hold up
             the weight of her family, but to do that, she needs Levi.
             She will have to give up her name and let him in completely
             or lose the best thing thats ever happened to her.
             For fans of Stephanie Perkins and Morgan Matson,
             THE COLOR PROJECT is a story about the three great loves of
             life family, friendship,
             and romance and the bonds that withstand tragedy.""",
             price="$2.99",
             rating="3.95/5",
             genre=genre2)

session.add(book3)
session.commit()


book4 = Book(user_id=1,
             picture="http://via.placeholder.com/400x500",
             name="Fallen Heir",
             author="Erin Watt",
             description="""These Royals will ruin you.
             Easton Royal has it all, looks, money, intelligence. His goal
             in life is to have as much fun as possible. He never thinks
             about the consequences because he does not have to.
             Until Hartley Wright appears, shaking up his easy life.
             She is the one girl who has said no, despite being attracted to
             him. Easton cannot figure her out and that makes her all the
             more irresistible. Hartley does not want him. She says he needs
             to grow up. She might be right.
             Rivals. Rules. Regrets. For the first time in Eastons life,
             wearing a Royal crown is not enough. He is about to learn
             that the higher you start, the harder you fall.""",
             price="$2.99",
             rating="4.02/5",
             genre=genre2)

session.add(book4)
session.commit()

# Mystery & Thriller - Books
genre3 = Genre(user_id=1, name="Mystery & Thriller")

session.add(genre3)
session.commit()

book1 = Book(user_id=1,
             picture="http://via.placeholder.com/400x500",
             name="The Good Daughter",
             author="Karin Slaughter",
             description="""Two girls are forced into the woods at
             gunpoint. One runs for her life. One is left behind.
             Twenty eight years ago, Charlotte and Samantha Quinns
             happy small town family life was torn apart by a
             terrifying attack on their family home. It left their
             mother dead. It left their father, Pikeville s notorious
             defense attorney devastated. And it left the
             family fractured beyond repair, consumed by secrets from
             that terrible night.
             Twenty eight years later, and Charlie has followed in her
             fathers footsteps to become a lawyer herself, the ideal
             good daughter. But when violence comes to Pikeville again
             and a shocking tragedy leaves the whole town traumatized.
             Charlie is plunged into a nightmare. Not only is she the
             first witness on the scene, but it is a case that unleashes
             the terrible memories she has spent so long trying to suppress.
             Because the shocking truth about the crime that destroyed her
             family nearly thirty years ago would not stay buried forever.""",
             price="$2.99",
             rating="4.23/5",
             genre=genre3)

session.add(book1)
session.commit()

book2 = Book(user_id=1,
             picture="http://via.placeholder.com/400x500",
             name="Emma in the Night",
             author="Wendy Walker",
             description="""From the bestselling author of All Is Not
             Forgotten comes a thriller about two missing sisters, a
             twisted family, and what happens when one girl comes back.
             One night three years ago, the Tanner sisters disappeared
             fifteen year old Cass and seventeen year old Emma.
             Three years later, Cass returns, without her sister Emma.
             Her story is one of kidnapping and betrayal, of a mysterious
             island where the two were held. But to forensic psychiatrist
             Dr. Abby Winter, something doesn't add up. Looking deep within
             this dysfunctional family Dr. Winter uncovers a life where
             boundaries were violated and a narcissistic parent held sway.
             And where one sister's return might just be the
             beginning of the crime.""",
             price="$2.99",
             rating="3.83/5",
             genre=genre3)

session.add(book2)
session.commit()

book3 = Book(user_id=1,
             picture="http://via.placeholder.com/400x500",
             name="I Know a Secret",
             author="Tess Gerritsen",
             description="""In the twelfth gripping novel featuring Jane
             Rizzoli and Maura Isles, the crime solving duo featured in
             the smash hit TNT series Rizzoli & Isles are faced with the
             gruesomely staged murder of a horror film producer.
             The crime scene is unlike any that Detective Rizzoli and
             medical examiner Maura Isles have ever before encountered.
             The woman lies in apparently peaceful repose on her bed,
             and Maura finds no apparent cause of death, but there is
             no doubt the woman is indeed dead. The victim eyes have
             been removed and placed in the palm of her hand, a gesture
             that echoes the terrifying films she produces. Is a crazed
             movie fan reenacting scenes from those disturbing films?
             When another victim is found, again with no apparent cause
             of death, again with a grotesquely staged crime scene, Jane
             and Maura realize the killer has widened his circle of
             targets. He is chosen one particular woman for his next
             victim, and she knows he is coming for her next. She is
             the only one who can help Jane and Maura catch the killer.
             But she knows a secret. And it is a secret she will never
             tell.""",
             price="$2.99",
             rating="4.27/5",
             genre=genre3)

session.add(book3)
session.commit()


book4 = Book(user_id=1,
             picture="http://via.placeholder.com/400x500",
             name="Girl in Snow",
             author="Danya Kukafka",
             description="""Who Are You When No One Is Watching?
             When a beloved high schooler named Lucinda Hayes is found
             murdered, no one in her sleepy Colorado suburb is untouched
             not the boy who loved her too much; not the girl who wanted
             her perfect life, not the officer assigned to investigate
             her murder. In the aftermath of the tragedy, these three
             indelible characters—Cameron, Jade, and Russ—must each
             confront their darkest secrets in an effort to find solace,
             the truth, or both. 
             In crystalline prose, Danya Kukafka offers a brilliant
             exploration of identity and of the razor sharp line between
             love and obsession, between watching and seeing, between truth
             and memory. Compulsively readable and powerfully moving, Girl
             in Snow offers an unforgettable reading experience and
             introduces a singular new talent in Danya Kukafka.""",
             price="$2.99",
             rating="3.48/5",
             genre=genre3)

session.add(book4)
session.commit()


# Non Fiction - Books
genre4 = Genre(user_id=1, name="Non Fiction")

session.add(genre4)
session.commit()


book1 = Book(user_id=1,
             picture="http://via.placeholder.com/400x500",
             name="The Diary of a Young Girl",
             author="Anne Frank, Eleanor Roosevelt",
             description="""Discovered in the attic in which she spent the
             last years of her life, Anne Frank's remarkable diary has since
             become a world classic a powerful reminder of the horrors of war
             and an eloquent testament to the human spirit.
             In 1942, with Nazis occupying Holland, a thirteen year old
             Jewish girl and her family fled their home in Amsterdam and went
             into hiding. For the next two years, until their whereabouts were
             betrayed to the Gestapo, they and another family lived cloistered
             in the 'Secret Annexe' of an old office building.
             Cut off from the outside world, they faced hunger, boredom, the
             constant cruelties of living in confined quarters, and the ever
             present threat of discovery and death. In her diary Anne Frank
             recorded vivid impressions of her experiences during this period.
             By turns thoughtful, moving, and amusing, her account offers a
             fascinating commentary on human courage and frailty and a
             compelling self portrait of a sensitive and spirited young woman
             whose promise was tragically cut short.""",
             price="$2.99",
             rating="4.1/5",
             genre=genre4)

session.add(book1)
session.commit()

book2 = Book(user_id=1,
             picture="http://via.placeholder.com/400x500",
             name="The Immortal Life of Henrietta Lacks",
             author="Rebecca Skloot",
             description="""Henrietta Lacks, as HeLa, is known to present day
             scientists for her cells from cervical cancer. She was a poor
             Southern tobacco farmer who worked the same land as her slave
             ancestors, yet her cells were taken without her knowledge and
             still live decades after her death.
             Cells descended from her may weigh more than 50M metric tons.
             HeLa cells were vital for developing the polio vaccine;
             uncovered secrets of cancer, viruses, and the atom bomb’s effects;
             helped lead to important advances like in vitro fertilization,
             cloning, and gene mapping; and have been bought and sold by the
             billions. Yet Henrietta Lacks was buried in an unmarked grave.
             The journey starts in the 'colored' ward of Johns Hopkins Hospital
             in the 1950s, her small, dying hometown of Clover, Virginia wooden
             slave quarters, faith healings, and voodoo. Today are stark white
             laboratories with freezers full of HeLa cells, East Baltimore
             children and grandchildren live in obscurity,
             see no profits, and feel violated. The dark history of
             experimentation on African Americans helped lead to the birth of
             bioethics, and legal battles over whether
             we control the stuff we are made of. """,
             price="$2.99",
             rating="4.04/5",
             genre=genre4)

session.add(book2)
session.commit()

book3 = Book(user_id=1,
             picture="http://via.placeholder.com/400x500",
             name="Bossypants",
             author="Tina Fey",
             description="""Before Liz Lemon, before 'Weekend Update,' before
             'Sarah Palin,' Tina Fey was just a young girl with a dream:
             a recurring stress dream that she was being chased through a
             local airport by her middle-school gym teacher. She also had a
             dream that one day she would be a comedian on TV.
             She has seen both these dreams come true.
             At last, Tina Fey's story can be told. From her youthful days
             as a vicious nerd to her tour of duty on Saturday Night Live;
             from her passionately halfhearted pursuit of physical beauty
             to her life as a mother eating things off the floor; from her
             one sided college romance to her nearly fatal honeymoon—from
             the beginning of this paragraph to this final sentence.

             Tina Fey reveals all, and proves what we've all suspected:
             you are no one until someone calls you bossy.
             (Includes Special, Never-Before-Solicited Opinions on
             Breastfeeding, Princesses, Photoshop, the Electoral Process,
             and Italian Rum Cake!)
             An unabridged recording on 5 CDs (5.5 Hours).""",
             price="$2.99",
             rating="3.94/5",
             genre=genre4)

session.add(book3)
session.commit()


book4 = Book(user_id=1,
             picture="http://via.placeholder.com/400x500",
             name="Into the Wild",
             author="Jon Krakauer",
             description="""In April 1992 a young man from a well to do
             family hitchhiked to Alaska and walked alone into the
             wilderness north of Mt. McKinley. His
             name was Christopher Johnson McCandless. He had given $25,000 in savings
             to charity, abandoned his car and most of his possessions, burned all the
             cash in his wallet, and invented a new life for himself. Four months later,
             a party of moose hunters found his decomposed body. How McCandless came to
             die is the unforgettable story of Into the Wild.
             Immediately after graduating from college in 1991, McCandless had roamed
             through the West and Southwest on a vision quest like those made by his
             heroes Jack London and John Muir. In the Mojave Desert he abandoned his car,
             stripped it of its license plates, and burned all of his cash. He would give
             himself a new name, Alexander Supertramp, and, unencumbered by money and
             belongings, he would be free to wallow in the raw, unfiltered experiences
             that nature presented. Craving a blank spot on the map, McCandless simply
             threw away the maps. Leaving behind his desperate parents and sister,
             he vanished into the wild. """,
             price="$2.99",
             rating="3.95/5",
             genre=genre4)

session.add(book4)
session.commit()

# Self Help - Books
genre5 = Genre(user_id=1, name="Self Help")

session.add(genre5)
session.commit()


book1 = Book(user_id=1,
             picture="http://via.placeholder.com/400x500",
             name="Big Magic: Creative Living Beyond Fear",
             author="Elizabeth Gilbert",
             description="""Readers of all ages and walks of life have drawn inspiration
             and empowerment from Elizabeth Gilbert’s books for years. Now this beloved
             author digs deep into her own generative process to share her wisdom and
             unique perspective about creativity. With profound empathy and radiant
             generosity, she offers potent insights into the mysterious nature of
             inspiration. She asks us to embrace our curiosity and let go of needless
             suffering. She shows us how to tackle what we most love, and how to face
             down what we most fear. She discusses the attitudes, approaches, and habits
             we need in order to live our most creative lives. Balancing between soulful
             spirituality and cheerful pragmatism, Gilbert encourages us to uncover the
             'strange jewels' that are hidden within each of us. Whether we are looking
             to write a book, make art, find new ways to address challenges in our work,
             embark on a dream long deferred, or simply infuse our everyday lives with
             more mindfulness and passion, Big Magic cracks open a world of wonder and joy.""",
             price="$2.99",
             rating="3.89/5",
             genre=genre5)

session.add(book1)
session.commit()

book2 = Book(user_id=1,
             picture="http://via.placeholder.com/400x500",
             name="Of Mess and Moxie: Wrangling Delight Out of This Wild and Glorious Life",
             author="Jen Hatmaker",
             description="""Jen Hatmaker believes backbone is the birthright of every woman.
             Women have been demonstrating resiliency and resolve since forever. They have
             incredibly strong shoulders to bear loss, hope, grief, and vision. She laughs
             at the days to come is how the ancient wisdom writings put it.
             But somehow women have gotten the message that pain and failure mean they must
             be doing things wrong, that they messed up the rules or tricks for a seamless
             life. As it turns out, every last woman faces confusion and loss, missteps
             and catastrophic malfunctions, no matter how much she is doing right.
             Struggle does not mean they are weak, it means they are alive.
             Jen Hatmaker, beloved author, Big Sister Emeritus, and Chief BFF, offers
             another round of hilarious tales, frank honesty, and hope for the woman
             who has forgotten her moxie. Whether discussing the grapple with change
             ("Everyone, be into this thing I am into! Except when I'm not. Then
             everyone be cool.") or the time she drove to the wrong city for a
             fourth grade field trip ("Why are we in San Antonio?"), Jen parlays her
             own triumphs and tragedies into a sigh of relief for all normal, fierce
             women everywhere who, like her, sometimes hide in the car eating crackers
             but also want to get back up and get back out, to live undaunted
             'in the moment' no matter what the moments hold.""",
             price="$2.99",
             rating="4.29/5",
             genre=genre5)

session.add(book2)
session.commit()

book3 = Book(user_id=1,
             picture="http://via.placeholder.com/400x500",
             name="Love Warrior",
             author="Glennon Doyle Melton",
             description="""The highly anticipated new memoir by bestselling author
             Glennon Doyle Melton tells the story of her journey of self-discovery
             after the implosion of her marriage.

             Just when Glennon Doyle Melton was beginning to feel she had it all
             figured out—three happy children, a doting spouse, and a writing
             career so successful that her first book catapulted to the top
             of the New York Times bestseller list—her husband revealed his
             infidelity and she was forced to realize that nothing was as it
             seemed. A recovering alcoholic and bulimic, Glennon found that
             rock bottom was a familiar place. In the midst of crisis, she
             knew to hold on to what she discovered in recovery: that her
             deepest pain has always held within it an invitation to a richer life.

             Love Warrior is the story of one marriage, but it is also the story
             of the healing that is possible for any of us when we refuse to
             settle for good enough and begin to face pain and love head on.
             This astonishing memoir reveals how our ideals of masculinity and
             femininity can make it impossible for a man and a woman to truly
             know one another and it captures the beauty that unfolds when one
             couple commits to unlearning everything they have been taught so
             that they can finally, after thirteen years of marriage, fall in love.
             Love Warrior is a gorgeous and inspiring account of how we are born
             to be warriors, strong, powerful, and brave; able to confront the
             pain and claim the love that exists for us all. This chronicle of
             a beautiful, brutal journey speaks to anyone who yearns for deeper,
             truer relationships and a more abundant, authentic life.""",
             price="$2.99",
             rating="4.09/5",
             genre=genre5)

session.add(book3)
session.commit()


book4 = Book(user_id=1,
             picture="http://via.placeholder.com/400x500",
             name="Lean In: Women, Work, and the Will to Lead",
             author="Sheryl Sandberg, Nell Scovell",
             description="""Sheryl Sandbergs Lean In is a massive cultural phenomenon
             and its title has become an instant catchphrase for empowering women.
             The book soared to the top of bestseller lists internationally, igniting
             global conversations about women and ambition. Sandberg packed theatres,
             dominated opinion pages, appeared on every major television show and on
             the cover of Time magazine, and sparked ferocious debate about women and
             leadership.
             Ask most women whether they have the right to equality at work and the
             answer will be a resounding yes, but ask the same women whether they
             had feel confident asking for a raise, a promotion, or equal pay, and
             some reticence creeps in.
             The statistics, although an improvement on previous decades, are
             certainly not in womens favour of 197 heads of state, only twenty two
             are women. Women hold just 20 percent of seats in parliaments globally,
             and in the world of big business, a meagre eighteen of the Fortune 500
             CEOs are women.
             In Lean In, Sheryl Sandberg Facebook COO and one of Fortune magazines
             Most Powerful Women in Business draws on her own experience of working
             in some of the worlds most successful businesses and looks at what
             women can do to help themselves, and make the small changes in their
             life that can effect change on a more universal scale.""",
             price="$2.99",
             rating="3.94/5",
             genre=genre5)

session.add(book4)
session.commit()
print("Added all books");
