from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt

# our home page view
def index(request):    
    return render(request, 'index.html')


def home(request):    
    return render(request, 'home.html')


# custom method for generating predictions
def getPredictions(tm,sm,cm,sym,fdm,tse,ase,sse,cse):


    txt1 = ['''Breakfast:

3 egg whites and 1 whole egg omelet with spinach, mushrooms, and onions
1 slice of whole wheat toast with avocado spread
1 cup of black coffee
Snack:

1 small apple
10 almonds
Lunch:

Grilled chicken breast with mixed greens salad (spinach, kale, arugula, lettuce) with cherry tomatoes, cucumber, and bell peppers, dressed with olive oil and vinegar
1 cup of brown rice
Snack:

1 small banana
1 tablespoon of peanut butter
Dinner:

Grilled salmon with roasted asparagus and sweet potatoes
1 cup of quinoa
Snack:

1 cup of Greek yogurt with mixed berries''','''Breakfast:

1 cup of oatmeal with mixed berries and almond milk
1 tablespoon of honey
1 cup of green tea
Snack:

1 small pear
10 walnuts
Lunch:

Grilled shrimp with mixed greens salad (spinach, kale, arugula, lettuce) with cherry tomatoes, cucumber, and bell peppers, dressed with olive oil and vinegar
1 cup of quinoa
Snack:

1 small orange
1 hard-boiled egg
Dinner:

Grilled chicken breast with roasted Brussels sprouts and sweet potatoes
1 cup of brown rice
Snack:

1 cup of cottage cheese with sliced peaches''','''Breakfast:

2 slices of whole wheat toast with mashed avocado and sliced tomatoes
1 cup of black coffee
Snack:

1 small apple
10 almonds
Lunch:

Grilled turkey burger with mixed greens salad (spinach, kale, arugula, lettuce) with cherry tomatoes, cucumber, and bell peppers, dressed with olive oil and vinegar
1 cup of brown rice
Snack:

1 small banana
1 tablespoon of almond butter
Dinner:

Grilled steak with roasted broccoli and sweet potatoes
1 cup of quinoa
Snack:

1 cup of Greek yogurt with mixed berries''']
    txt2 = ['''Breakfast:

3-4 egg whites scrambled with vegetables (spinach, bell peppers, mushrooms)
1 slice of whole-grain toast
1 small avocado
1 cup of black coffee or green tea
Snack:

1 medium apple
1 tbsp of almond butter
Lunch:

Grilled chicken breast or salmon
1 cup of brown rice or quinoa
1 cup of mixed vegetables (broccoli, asparagus, carrots)
1 small green salad with olive oil and vinegar dressing
Snack:

1 small protein shake with almond milk or water
1 medium banana
Dinner:

Grilled steak or tofu
1 sweet potato or baked potato
1 cup of mixed vegetables (zucchini, cauliflower, Brussels sprouts)
1 small green salad with olive oil and vinegar dressing
Before Bed:

1 cup of low-fat Greek yogurt
1 tbsp of chia seeds''','''Breakfast:

3 scrambled eggs
1 slice of whole-grain toast
1/2 avocado
1 cup of berries
1 cup of coffee or tea
Mid-Morning Snack:

1 apple
1 oz of almonds or walnuts
Lunch:

Grilled chicken breast
1/2 cup of brown rice
1 cup of mixed vegetables (broccoli, carrots, and green beans)
1 small salad with olive oil and vinegar dressing
Afternoon Snack:

1/2 cup of Greek yogurt
1/2 cup of mixed berries
1 tablespoon of honey
Dinner:

Grilled salmon fillet
1 cup of roasted sweet potatoes
1 cup of steamed broccoli
1 small salad with olive oil and vinegar dressing
Before Bed Snack:

1 cup of cottage cheese
1/2 cup of mixed berries''','''Breakfast

3 whole eggs
1 cup of spinach
1 medium avocado
1 slice of whole-grain toast
Mid-Morning Snack

1 apple
1 tablespoon of almond butter
Lunch

4 oz grilled chicken breast
1 cup of mixed vegetables (broccoli, bell peppers, carrots)
1/2 cup of brown rice
Afternoon Snack

1 serving of Greek yogurt (plain)
1/4 cup of blueberries
Dinner

4 oz grilled salmon
1 cup of roasted Brussels sprouts
1 small sweet potato
Evening Snack

1/2 cup of cottage cheese
1/4 cup of mixed nuts (almonds, walnuts, cashews)
''']
    txt3=['''Breakfast: Scrambled eggs with spinach and cherry tomatoes, whole-grain toast, and fresh fruit.

Snack: Greek yogurt with berries and a handful of nuts.

Lunch: Grilled chicken salad with mixed greens, avocado, and a balsamic vinaigrette dressing.

Snack: Sliced apple with almond butter.

Dinner: Grilled salmon with roasted vegetables (such as zucchini, bell peppers, and asparagus) and a side of quinoa.''','''Breakfast: Overnight oats with sliced banana, chia seeds, and honey.

Snack: Carrot sticks with hummus.

Lunch: Turkey wrap with lettuce, tomato, avocado, and mustard, and a side of fruit.

Snack: Greek yogurt with granola and mixed berries.

Dinner: Grilled sirloin steak with sweet potato wedges and a side salad.''','''Breakfast: Avocado toast with sliced tomato and a poached egg.

Snack: Edamame beans with sea salt.

Lunch: Tuna salad with mixed greens, cucumber, and cherry tomatoes.

Snack: Sliced pear with cheese.

Dinner: Grilled chicken kebabs with mixed vegetables and brown rice.''']
    txt4=['''Breakfast:

1 whole-grain English muffin with scrambled eggs, cheese, and sliced tomato
Snack:

1 small orange
1 ounce of almonds
Lunch:

Grilled shrimp kebab with bell pepper, onion, and zucchini
1 cup of quinoa salad with mixed greens, cherry tomatoes, and feta cheese
Snack:

Cottage cheese with sliced peaches
Dinner:

Baked chicken breast with garlic and rosemary
Roasted Brussels sprouts
Quinoa pilaf''','''Breakfast:

Overnight oats made with rolled oats, almond milk, chia seeds, and mixed berries
Snack:

1 small banana
1 tablespoon of peanut butter
Lunch:

Grilled chicken salad with mixed greens, cherry tomatoes, cucumber, and balsamic vinaigrette dressing
Snack:

1 cup of vegetable sticks (carrots, celery, bell pepper) with hummus
Dinner:

Grilled sirloin steak
Roasted sweet potato
Sautéed spinach''','''Breakfast:

2 scrambled eggs
1 slice of whole-grain toast
1 small avocado
Snack:

1 medium apple
1 tablespoon of almond butter
Lunch:

Grilled chicken breast
1 cup of brown rice
Steamed broccoli
Snack:

Greek yogurt with mixed berries
Dinner:

Grilled salmon
1 cup of quinoa
Roasted asparagus''']
    txt5=['''Breakfast:

Greek yogurt with granola and berries
1 hard-boiled egg
Snack:

1 small orange
1 ounce of pistachios
Lunch:

Grilled chicken breast
Brown rice
Steamed green beans
1 small banana
Snack:

1 small Greek yogurt with berries
Dinner:

Grilled shrimp
Roasted zucchini
Quinoa
1 small peach''','''Breakfast:

Oatmeal with banana slices and cinnamon
1 hard-boiled egg
Snack:

1 small pear
1 ounce of walnuts
Lunch:

Tuna salad with mixed greens, tomatoes, and cucumber
Whole-grain pita
1 medium-sized apple
Snack:

1 small cottage cheese with baby carrots
Dinner:

Grilled lean steak
Roasted asparagus
Quinoa
1 small apple''','''Breakfast:

2 scrambled eggs with spinach and mushrooms
1 slice of whole-grain toast
1 medium-sized orange
Snack:

1 small apple
1 ounce of almonds
Lunch:

Grilled chicken breast
Brown rice
Steamed broccoli
1 small banana
Snack:

1 small Greek yogurt with berries
Dinner:

Grilled salmon
Roasted sweet potato
Steamed green beans
1 small peach''']
    txt6=['''Breakfast:

1 cup low-fat cottage cheese with sliced strawberries and a tablespoon of honey
1 slice of whole-grain toast
1 cup of green tea
Snack:

1 small apple
1 tablespoon of peanut butter
Lunch:

Grilled chicken breast with quinoa salad (quinoa, spinach, red onion, and cherry tomatoes)
1 tablespoon of olive oil and vinegar dressing
1 small whole-grain roll
1 cup of water
Snack:

1 small low-fat Greek yogurt with a handful of mixed berries
Dinner:

Grilled shrimp with roasted vegetables (zucchini, eggplant, and red onion)
1/2 cup brown rice
1 cup of water''','''Breakfast:

2 scrambled eggs
1 slice of whole-grain toast with 1 tablespoon of avocado spread
1 small orange
1 cup of green tea
Snack:

1 small banana
1 tablespoon of almond butter
Lunch:

Turkey and avocado wrap (whole-grain tortilla, turkey breast, avocado, lettuce, and tomato)
1 small pear
1 cup of water
Snack:

1 small low-fat Greek yogurt with a handful of mixed berries
Dinner:

Baked chicken breast with steamed vegetables (asparagus, green beans, and bell peppers)
1 small sweet potato
1 cup of water''','''Breakfast:

1 cup oatmeal with sliced banana and a tablespoon of honey
1 boiled egg
1 cup green tea
Snack:

1 apple with a tablespoon of peanut butter
Lunch:

Grilled chicken breast with mixed greens salad (lettuce, cucumber, cherry tomatoes, and red onion)
1 tablespoon of olive oil and vinegar dressing
1 small whole-grain roll
1 cup of water
Snack:

1 small low-fat Greek yogurt with a handful of mixed berries
Dinner:

Grilled salmon fillet with roasted vegetables (broccoli, carrots, and cauliflower)
1/2 cup brown rice
1 cup of water''']
    import joblib,random
    model = joblib.load("model.joblib")
    
    prediction = model.predict([[tm,sm,cm,sym,fdm,tse,ase,sse,cse]])
    t = "BodyFat : "+str(prediction[0])
    if prediction[0]<=8:
        t+='\n\n'+random.choice(txt1)+"""\n\nExcerises---------\n
1. Resistance training: Incorporate weight training into your routine to help maintain and build muscle mass. This can include exercises such as squats, deadlifts, bench presses, and pull-ups.

2. High-intensity interval training (HIIT): HIIT workouts can help burn fat and improve cardiovascular health. This can include exercises such as sprints, burpees, and jump squats.

3. Plyometric exercises: These exercises involve explosive movements that can help improve power and speed. Examples include jump lunges, box jumps, and explosive push-ups.

4. Yoga and Pilates: These practices can help improve flexibility and mobility, while also providing a low-impact workout that can be beneficial for recovery and injury prevention."""
    elif prediction[0]>8 and prediction[0]<=10:
        t+='\n\n'+random.choice(txt2)+"""\n\nExcerises---------\n
1. Resistance Training: Resistance training, also known as weight training, is an effective way to build and maintain lean muscle mass. This type of exercise involves using weights, resistance bands, or bodyweight exercises to challenge your muscles and increase strength. Examples of resistance exercises include squats, deadlifts, bench presses, pull-ups, and push-ups.

2. High-Intensity Interval Training (HIIT): HIIT involves alternating periods of high-intensity exercise with short rest periods. This type of workout can be an effective way to burn fat while preserving muscle mass. Examples of HIIT exercises include sprints, burpees, and jump squats.

3. Cardiovascular Exercise: Cardiovascular exercise is important for overall fitness and can also be effective for burning fat. Activities such as running, cycling, swimming, or rowing can be good options for individuals with low body fat levels. However, it is important to not overdo it with cardio exercise, as too much can result in muscle loss.

4. Compound Movements: Compound movements involve using multiple muscle groups at once and can be a great way to build overall strength and muscle mass. Examples of compound exercises include squats, lunges, deadlifts, and bench presses.

5. Core Strengthening: Strong core muscles are important for overall fitness and can also help to prevent injury. Exercises such as planks, crunches, and Russian twists can help to strengthen the core."""
    elif prediction[0]>10 and prediction[0]<=15:
        t+='\n\n'+random.choice(txt3)+"""\n\nExcerises---------\n
1. Deadlifts - Deadlifts are a great exercise for building overall strength and targeting the
muscles in your legs, glutes, and back.
2. Squats - Squats are another compound exercise that target the muscles in your legs,
glutes, and core. They are also great for building lower body strength.
3. Bench press - The bench press is a classic exercise that primarily targets your chest
muscles, but also works your triceps and shoulders.
4. Pull-ups - Pull-ups are a great upper body exercise that work your back, shoulders, and
arms. If you can't do a full pull-up, you can start with assisted pull-ups or chin-ups.
5. Lunges - Lunges are a unilateral exercise that target your legs and glutes They are also
great for improving your balance and stability.
6. Overhead press - The overhead press targets your shoulders, but also works your triceps
and upper back muscles. It's a great exercise for building upper body strength and size.
7. Rows - Rows are a great exercise for targeting your back muscles, which are often
neglected in training. They can help improve your posture and prevent back pain.
8. Plank - Planks are a great exercise for building core strength and stability. They also help
improve your overall posture and can reduce your risk of back pain."""
    elif prediction[0]>15 and prediction[0]<=20:
        t+='\n\n'+random.choice(txt4)+"""\n\nExcerises---------\n
1. Turkish Get-Ups - This exercise involves standing up from a lying position while holding a
weight and can help improve core strength and stability.
2. Farmer's Walk - This exercise involves carrying heavyweights in each hand and can help
improve grip strength, core stability, and overall strength.
3. Dragon Flags - This challenging core exercise involves lifting the entire body off the
ground while keeping the core engaged.
4. Pistol Squats - This unilateral exercise involves squatting on one leg and can help
improve balance and lower body strength.
5. Kettlebell Swings - This explosive exercise targets the glutes hamstrings, and lower back
and can help improve power and strength."""
    elif prediction[0]>20 and prediction[0]<=30:
        t+='\n\n'+random.choice(txt5)+"""\n\nExcerises---------\n
1. High-Intensity Interval Training (HIIT): This type of training involves short bursts of high-
intensity exerciser followed by periods of rest or low-intensity exercise. It can be done
with a variety of exercises such as running, cycling, or bodyweight exercises.
2. Resistance Training: Strength training with weights or resistance bands can help build
muscle mass, which can increase your metabolism and burn more calories.
3, Plyometric Exercises: These are high-impact exercises that involve explosive movements,
such as jumping or hopping. They can help increase your heart rate and bum calories.
4. Tabata Training: This is a form of HIIT that involves doing 20 seconds of high-intensity
exerciser followed by IO seconds of rest, for a total of 4 minutes. It can be done with a
variety of exercises, such as burpees, squats, or push-ups.
5. Cardiovascular Exercises: Any form of cardio exercise, such as running, swimming, or
cycling, can help you burn calories and reduce body fat.
6 Rare exercises: There are some exercises that are not commonly seen in gyms, but can
still be effective at burning fat and building muscle. These include exercises such as sled
pushes/pulls, battle ropes, kettlebell swings, and sandbag carries."""
    else:
        t+='\n\n'+random.choice(txt6)+"""\n\n---------Excerises---------\n
1. Walking: Walking is a low-impact exercise that is easyto do and can help you bum
calorie-x
2. Cycling: Cycling is another low-impact exercise that can be done indoors or outdoors. It's
a great way to get your heart rate up and burn calories.
3. Swimming: Swimming is a great full-body workout that is easy on the joints. It's also a
great way to cool off on a hot day.
4. High-Intensity Interval Training (HIIT): HIIT is a type of workout that involves short bursts
of intense exercise followed by periods of rest It's a great way to burn calories and
improve your cardiovascular health.
5. Resistance Training: Resistance training can help build muscle and increase your
metabolism. This can help you bum more calories even when you're not working out."""
    return t

@csrf_exempt
# our result page view
def result(request):
    if request.method == 'POST':
        result = getPredictions(float(request.POST.get('a1')),
                                float(request.POST.get('a3')),
                                float(request.POST.get('a4')),
                                float(request.POST.get('a5')),
                                float(request.POST.get('a6')),
                                float(request.POST.get('a7')),
                                float(request.POST.get('a8')),
                                float(request.POST.get('a9')),
                                float(request.POST.get('a10')))

        return render(request, 'result.html', {'result':result})
