from datetime import datetime
from decimal import Decimal
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render,get_object_or_404, redirect
from django.conf import settings
from pip._internal.resolution.resolvelib import provider

from .models import Users, Categories, Subcategories, Store, Providers, Cart, OrderDetails, Orders, Measure_units


def index(request):
    settings.GLOBAL_VARIABLE = ""
    return render(request, 'account_pages/index.html')


def registration(request):
    return render(request, 'account_pages/registration_page.html')


def login(request, message=None):
    context = {}
    if message:
        context['message'] = message
    return render(request, 'account_pages/login_page.html', context)


def modify_data_account(request, message=None):
    if settings.GLOBAL_VARIABLE == "":
        return render(request, 'account_pages/index.html', {'message': 'Devi accedere per arrivare a questa pagina'})

    username_user = settings.GLOBAL_VARIABLE
    type_user = settings.GLOBAL_TYPE_USER

    account_data = get_data_account(username_user)

    context = {
        'account_data': account_data,
        'message': message,
        'type_user': type_user,
        'show_update_form': False,  # Imposta inizialmente il flag per mostrare il form di aggiornamento a False
        'show_confirm_form': True   # Imposta inizialmente il flag per mostrare il form di conferma a True
    }
    if message == 'Password Corretta':
        context['show_update_form'] = True  # Se il messaggio è "Password Corretta", mostra il form di aggiornamento
        context['show_confirm_form'] = False  # Nascondi il form di conferma
    else:
        # Se il messaggio è "Password Errata", mantieni il form di conferma e nascondi il form di aggiornamento
        context['show_update_form'] = False
        context['show_confirm_form'] = True

    return render(request, 'account_pages/modify_data_account_page.html', context)


def homepage_client(request, message=None):
    if settings.GLOBAL_VARIABLE == "":
        return render(request, 'account_pages/index.html', {'message': 'Devi accedere per arrivare a questa pagina'})
    categories = Categories.objects.all()
    providers = Providers.objects.all()
    options_data_cat = []
    options_data_prov = []

    for category in categories:
        store_data = get_store_data(category.name)
        options_data_cat.append({
            'id': category.id,
            'name': category.name,
            'store_data': store_data
        })

    for provider in providers:
        options_data_prov.append({
            'id_provider': provider.id,
            'name_provider': provider.username,
        })

    context = {
        'options_data_cat': options_data_cat,
        'options_data_prov': options_data_prov,
        'show_options': True,
    }
    if message is not None and isinstance(message, str) and message.strip() != "":
        context['message'] = message

    return render(request, 'client/homepage_client.html', context)


def homepage_provider(request, message=None):
    if settings.GLOBAL_VARIABLE == "":
        return render(request, 'account_pages/index.html', {'message': 'Devi accedere per arrivare a questa pagina'})
    categories = Categories.objects.all()
    options_data_cat = []

    for category in categories:
        store_data = get_store_data_for_prov(category.name)
        options_data_cat.append({
            'id': category.id,
            'name': category.name,
            'store_data': store_data
        })

    context = {
        'options_data_cat': options_data_cat,
        'show_options': True,
    }
    if message is not None and isinstance(message, str) and message.strip() != "":
        context['message'] = message
    return render(request, 'provider/homepage_provider.html', context)


def forgot_psw(request):
        return render(request, 'account_pages/forgot_password.html')


def delete_acc_page(request):
    if settings.GLOBAL_VARIABLE == "":
        return render(request, 'account_pages/index.html', {'message': 'Devi accedere per arrivare a questa pagina'})
    username = settings.GLOBAL_VARIABLE
    type = settings.GLOBAL_TYPE_USER
    context = {
        'username': username,
        'type': type,
    }
    return render(request, 'account_pages/delete_account.html', context)


def cart(request, message=None):
    if not settings.GLOBAL_VARIABLE:
        return render(request, 'account_pages/index.html', {'message': 'Devi accedere per arrivare a questa pagina'})

    cart_data = get_cart_data(settings.GLOBAL_VARIABLE)

    context = {
        'cart_data': cart_data  # Assicurati che qui stai passando i dati del carrello senza incorrere in sovrascritture accidentali
    }
    if message:
        context['message'] = message
    return render(request, 'client/cart_page.html', context)


def modify_data_store(request, store_id):
    if settings.GLOBAL_VARIABLE == "":
        return render(request, 'account_pages/index.html', {'message': 'Devi accedere per arrivare a questa pagina'})

    store_data = get_data_product(store_id)

    context = {
        'store_data': store_data,
    }

    return render(request, 'provider/modify_product_page.html', context)


def orders(request, message=None):
    if not settings.GLOBAL_VARIABLE:
        return render(request, 'account_pages/index.html', {'message': 'Devi accedere per arrivare a questa pagina'})

    orders_data = get_orders_data(settings.GLOBAL_VARIABLE)

    context = {
        'orders_data': orders_data  # Assicurati che qui stai passando i dati del carrello senza incorrere in sovrascritture accidentali
    }
    if message:
        context['message'] = message
    return render(request, 'client/orders_page_client.html', context)


def order_details(request, order_id):
    if not settings.GLOBAL_VARIABLE:
        return render(request, 'account_pages/index.html', {'message': 'Devi accedere per arrivare a questa pagina'})

    orders_details_data = get_order_details_data(order_id)

    context = {
        'orders_details_data': orders_details_data  # Assicurati che qui stai passando i dati del carrello senza incorrere in sovrascritture accidentali
    }

    return render(request, 'client/order_details_page_client.html', context)


def update_psw_page(request):
    username = request.GET.get('username')
    if username:
        # La logica per l'aggiornamento della password va qui
        return render(request, 'account_pages/update_psw.html', {'username': username})
    else:
        return redirect('forgot_password')  # Reindirizza alla pagina di recupero password se non c'è username


def controlla_dati(request):
    if request.method == 'POST':
        type = request.POST.get('user_type')
        username_user = request.POST.get('username')
        psw_user = request.POST.get('psw')
        try:
            if type == "C":
                user = Users.objects.get(username=username_user)
            else:
                user = Providers.objects.get(username=username_user)
            if check_password(psw_user, user.password):
                settings.GLOBAL_TYPE_USER = type
                settings.GLOBAL_VARIABLE = username_user
                if type == "C":
                    return JsonResponse({"successo": True, "redirect_url": "/homepage_client/"})
                else:
                    return JsonResponse({"successo": True, "redirect_url": "/homepage_provider/"})

            else:
                return JsonResponse({"successo": False, "messaggio": "Password Errata"})
        except Users.DoesNotExist:
            return JsonResponse({"successo": False, "messaggio": "Utente non trovato"})
    return JsonResponse({"successo": False, "messaggio": "Metodo non supportato"})


def controlla_username(request):
    if request.method == 'POST':
        type = request.POST.get('user_type')
        username = request.POST.get('username')
        if type == "C":
            if Users.objects.filter(username=username).exists():
                user = Users.objects.get(username=username)
            else:
                return render(request, 'account_pages/forgot_password.html', {'message': 'Username non trovato'})
        else:
            if Providers.objects.filter(username=username).exists():
                user = Providers.objects.get(username=username)
            else:
                return render(request, 'account_pages/forgot_password.html', {'message': 'Username non trovato'})

        email = user.email

        # Configura i dettagli dell'email
        oggetto = "Cambio password"
        messaggio = "Clicca sul link per cambiare la password: https://esame-ppm-2.vercel.app/update_psw_page/?username=" + username
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]

        # Invia l'email
        send_mail(oggetto, messaggio, email_from, recipient_list)

        return render(request, 'account_pages/login_page.html', {'message': 'Ti è stata inviata una mail col link per cambiare la password'})

    return JsonResponse({"successo": False, "messaggio": "Metodo non supportato"})


def do_registation(request):
    if request.method == 'POST':
        type = request.POST.get('user_type')
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['psw']
        if type=="C":
            if Users.objects.filter(username=username).exists() or Users.objects.filter(email=email):
                return render(request, 'account_pages/registration_page.html', {'message': 'Username o email già esistente'})
        else:
            if Providers.objects.filter(username=username).exists() or Providers.objects.filter(email=email):
                return render(request, 'account_pages/registration_page.html', {'message': 'Username o email già esistente'})
        try:
            hashed_password = make_password(password)
            # Creazione dell'utente
            if type=="C":
                Users.objects.create(email=email, username=username, password=hashed_password, type=type)
            else:
                Providers.objects.create(email=email, username=username, password=hashed_password, type=type)
            return render(request, 'account_pages/index.html', {'message': 'Account creato'})
        except IntegrityError:
            return JsonResponse({"successo": False, "messaggio": "Errore nel creare l'utente"})

    return JsonResponse({"successo": False, "messaggio": "Metodo non supportato"})


def update_psw(request):
    if request.method == 'POST':
        type = request.POST.get('type')
        username = request.POST.get('username')
        new_psw = request.POST.get('psw')
        hashed_password = make_password(new_psw)
        try:
            if type=="C":
                user_profile = get_object_or_404(Users, username=username)
            else:
                user_profile = get_object_or_404(Providers, username=username)

            user_profile.password = hashed_password
            user_profile.save()
            return render(request, 'account_pages/index.html', {'message': 'Password aggiornata con successo.'})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False, "message": "Metodo non supportato."})


def get_subcategories(request):
    category_name = request.GET.get('category')

    try:
        category = Categories.objects.get(name=category_name)
    except Categories.DoesNotExist:
        return JsonResponse([], safe=False)

    subcategories = Subcategories.objects.filter(category=category).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)


def get_store_data(category_name):
    store_data = []

    try:
        category = Categories.objects.get(name=category_name)
    except Categories.DoesNotExist:
        # Gestisci il caso in cui la categoria non esista
        return store_data

    subcategories = Subcategories.objects.filter(category=category)
    for subcategory in subcategories:
        stores = Store.objects.filter(subcategory=subcategory)

        for store in stores:
            measure_unit = store.measure_units.abbreviation
            provider_username = store.provider.username  # Accedi al campo username di Providers
            subcategory_name = subcategory.name  # Accedi direttamente al nome della sottocategoria
            price = store.price_product
            description = store.desc_prod
            if store.discount is None:
                discount = ""
            else:
                discount = f"{store.discount}%"
            av_quant = store.available_quantity
            id_store = store.id
            store_data.append({
                'fornitore_username': provider_username,
                'sottocategoria_nome': subcategory_name,
                'prezzo': price,
                'descrizione': description,
                'sconto': discount,
                'quantita_disponibile': f"{av_quant} {measure_unit}",
                'id_store': id_store,
            })

    return store_data


def get_store_data_for_single_cat(request):
    if request.method == 'GET':
        category_name = request.GET.get('category', '')
        store_data = []

        try:
            category = Categories.objects.get(name=category_name)
        except Categories.DoesNotExist:
            # Gestisci il caso in cui la categoria non esista
            return JsonResponse(store_data, safe=False)

        subcategories = Subcategories.objects.filter(category=category)
        for subcategory in subcategories:
            stores = Store.objects.filter(subcategory=subcategory)

            for store in stores:
                measure_unit = store.measure_units.abbreviation
                provider_username = store.provider.username  # Accedi al campo username di Providers
                subcategory_name = subcategory.name  # Accedi direttamente al nome della sottocategoria
                price = store.price_product
                description = store.desc_prod
                if store.discount is None:
                    discount = ""
                else:
                    discount = f"{store.discount}%"
                av_quant = store.available_quantity
                id_store = store.id
                store_data.append({
                    'fornitore_username': provider_username,
                    'sottocategoria_nome': subcategory_name,
                    'prezzo': price,
                    'descrizione': description,
                    'sconto': discount,
                    'quantita_disponibile': f"{av_quant} {measure_unit}",
                    'id_store': id_store,
                })

        return JsonResponse(store_data, safe=False)


def get_store_data_for_single_subcat_or_prov(request):
    if request.method == 'GET':
        subcategory_id = request.GET.get('subcategory_id', '')
        provider_username = request.GET.get('provider', '')
        # Inizializza una query di filtro per il modello Store
        filter_query = Q()

        # Aggiungi la clausola di filtro per la sottocategoria, se specificata
        if subcategory_id:
            filter_query &= Q(subcategory_id=subcategory_id)

        # Aggiungi la clausola di filtro per il fornitore, se specificato
        if provider_username:
            filter_query &= Q(provider__username=provider_username)

        # Esegue la query per ottenere i negozi filtrati
        stores = Store.objects.filter(filter_query)

        store_data = []

        for store in stores:
            measure_unit = store.measure_units.abbreviation
            # Ottieni i dettagli del negozio
            provider_username = store.provider.username
            subcategory_name = store.subcategory.name
            price = store.price_product
            description = store.desc_prod
            av_quant = store.available_quantity
            discount = f"{store.discount}%" if store.discount else ""  # Gestisci il caso in cui lo sconto sia None
            id_store = store.id

            # Aggiungi i dettagli del negozio alla lista dei dati del negozio
            store_data.append({
                'fornitore_username': provider_username,
                'sottocategoria_nome': subcategory_name,
                'prezzo': price,
                'descrizione': description,
                'sconto': discount,
                'quantita_disponibile': f"{av_quant} {measure_unit}",
                'id_store': id_store,
            })

    return JsonResponse(store_data, safe=False)


def insert_into_cart(request, store_id):
    if request.method == 'GET': # Recupera l'id dello store dal POST data
        # Controllo se lo store esiste
        store = get_object_or_404(Store, pk=store_id)

        # Recupera l'username dell'utente dal request (suppongo che tu abbia già autenticato l'utente)
        username_user = settings.GLOBAL_VARIABLE

        # Recupera l'utente dal database
        utente = get_object_or_404(Users, username=username_user)


        # Cerca se il prodotto è già nel carrello dell'utente
        if Cart.objects.filter(user=utente, store=store).exists():
            return homepage_client(request, 'Prodotto già nel carrello')

        # Se il prodotto non è già nel carrello, aggiungilo
        Cart.objects.create(user=utente, store=store, quantity=0)

        return homepage_client(request, 'Prodotto inserito nel carrello')

    # Se la richiesta non è POST, ritorna un messaggio di errore
    return JsonResponse({"successo": False, "messaggio": "Metodo non supportato"})


def get_cart_data(username):
    cart_data = []

    if not username:
        return JsonResponse({'error': 'Username is required'}, status=400)

    user = get_object_or_404(Users, username=username)

    cart_items = Cart.objects.filter(user=user).select_related('store')
    for item in cart_items:
        store = item.store
        if store.discount is None:
            discount = ""
        else:
            discount = f"{store.discount}%"
        cart_data.append({
            'fornitore_nome': store.provider.username,
            'descrizione': store.desc_prod,
            'prezzo': store.price_product,
            'sconto': discount,
            'quantita_disponibile': f"{store.available_quantity} {store.measure_units.abbreviation}",
            'cart_id': item.id,
        })

    return cart_data


def delete_one_prod_form_cart(request, cart_id):
    if request.method == 'GET': # Recupera l'id dello store dal POST data
        # Recupera l'username dell'utente dal request (suppongo che tu abbia già autenticato l'utente)
        username_user = settings.GLOBAL_VARIABLE

        # Recupera il carrello dall'ID fornito
        cart_to_eliminate = get_object_or_404(Cart, pk=cart_id)
        # Controlla se il carrello appartiene all'utente autenticato
        if cart_to_eliminate.user.username == username_user:
            # Elimina l'oggetto cart dal database
            cart_to_eliminate.delete()
            return cart(request, 'Prodotto eliminato dal carrello')

    # Se la richiesta non è POST, ritorna un messaggio di errore
    return JsonResponse({"successo": False, "messaggio": "Metodo non supportato"})


def do_order(request):
    if request.method == 'POST':
        # Estrai i valori di quantità dalla richiesta POST
        quantities = request.POST.getlist('quantity[]')  # [] per ottenere una lista di valori

        username = settings.GLOBAL_VARIABLE
        user = get_object_or_404(Users, username=username)

        cart_items = Cart.objects.filter(user=user)

        order = Orders.objects.create(user=user, status="S", date_order=timezone.now().timestamp())

        for item, quantity in zip(cart_items, quantities):
            order_detail = OrderDetails(quantity=quantity, store=item.store, order=order, status="S")
            order_detail.save()
            item.delete()

        return cart(request, 'Ordine Effettuato')

    return JsonResponse({"successo": False, "messaggio": "Metodo non supportato"})


def get_orders_data(username):
    orders_data = []

    if not username:
        return JsonResponse({'error': 'Username is required'}, status=400)

    user = get_object_or_404(Users, username=username)

    orders_items = Orders.objects.filter(user=user).order_by('-date_order')
    for item in orders_items:
        timestamp = float(item.date_order)
        date_time = datetime.fromtimestamp(timestamp)
        date_only = date_time.strftime('%d.%m.%Y %H:%M')
        if item.status=="S" :
            txt_status = "In sospeso"
        elif item.status=="C" :
            txt_status = "Completato"
        order_info = {
            'status': txt_status,
            'order_id': item.id,
            'data': date_only,
        }
        orders_data.append(order_info)

    return orders_data


def get_order_details_data(order_id):
    order_details_data = []

    order = get_object_or_404(Orders, pk=order_id)

    order_details_items = OrderDetails.objects.filter(order=order)
    for item in order_details_items:
        store = item.store
        price_product = Decimal(str(store.price_product))
        price = price_product * item.quantity
        if item.status=="S" :
            txt_status = "In sospeso"
        elif item.status=="A" :
            txt_status = "Accettato"
        else:
            txt_status = "Rifiutato"
        if store.discount is None:
            price_discounted = 0
            discount = ""
        else:
            price_discounted = (price_product * (1 - Decimal(store.discount) / 100)) * item.quantity
            discount = f"{store.discount}%"
        order_details_info = {
            'status_order': order.status,
            'order_id': order.id,
            'quantita': f"{item.quantity} {store.measure_units.abbreviation}",
            "prezzo_totale": f"{price:.2f}",
            'prezzo_totale_scontato': f"{price_discounted:.2f}",
            'descrizione': store.desc_prod,
            'sconto': discount,
            'status': txt_status,
            'fornitore_nome': store.provider.username,
        }
        order_details_data.append(order_details_info)

    return order_details_data


def cancel_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id', '')
        order = get_object_or_404(Orders, pk=order_id)
        order_details_items = OrderDetails.objects.filter(order=order, status="S")
        for item in order_details_items:
                item.delete()

        order_details_items = OrderDetails.objects.filter(order=order)
        if len(order_details_items) == 0:
            order.delete()
        else:
            order.status="C"
            order.save()

        return orders(request, 'Ordine cancellato')
    else:
        return orders(request, 'Metodo non consentito')


def control_psw(request):
    if request.method == 'POST':
        username = settings.GLOBAL_VARIABLE
        type = settings.GLOBAL_TYPE_USER
        psw = request.POST.get('psw', '')

        try:
            if type=="C":
                user = Users.objects.get(username=username)
            else:
                user = Providers.objects.get(username=username)
            if check_password(psw, user.password):
                return modify_data_account(request, 'Password Corretta')
            else:
                return modify_data_account(request, 'Password Errata')
        except Users.DoesNotExist:
            return JsonResponse({"successo": False, "messaggio": "Utente non trovato"})

    return JsonResponse({"successo": False, "messaggio": "Metodo non supportato"})


def get_data_account(username_user):
    account_data = []
    type_user = settings.GLOBAL_TYPE_USER
    if type_user=="C":
        user = get_object_or_404(Users, username=username_user)
        user_items = Users.objects.filter(pk=user.id)
    else:
        user = get_object_or_404(Providers, username=username_user)
        user_items = Providers.objects.filter(pk=user.id)

    for item in user_items:
        user_info = {
            'email': item.email,
            'username': item.username,
        }
        account_data.append(user_info)

    return account_data


def update_datas_account(request):
    if request.method == 'POST':
        old_username = settings.GLOBAL_VARIABLE
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')

        # Ottieni l'utente attuale per escluderlo dalla query
        current_user = Users.objects.get(username=old_username)

        # Controlla se esiste già un altro utente con lo stesso username
        if Users.objects.exclude(id=current_user.id).filter(username=username).exists() or Users.objects.exclude(id=current_user.id).filter(email=email).exists():
            return modify_data_account(request, "Impossibile modificare i dati perchè esise già un account con quella email o username")
        else:
            settings.GLOBAL_VARIABLE = username
            current_user.username = username
            current_user.email = email
            current_user.save()
            return homepage_client(request, "Dati modificati con successo")

    # Gestisci il caso in cui il metodo della richiesta non sia POST
    return JsonResponse({"successo": False, "messaggio": "Metodo non supportato"})


def delete_account(request):
    if request.method == 'POST':
        username = settings.GLOBAL_VARIABLE
        type = settings.GLOBAL_TYPE_USER
        psw = request.POST.get('psw', '')

        try:
            if type=="C":
                user = Users.objects.get(username=username)
                orders_items = Orders.objects.filter(user=user)
                for item in orders_items:
                    if item.status=="S" :
                        return homepage_client(request, "Impossibile cancellare il tuo account, è presente un ordine in sospeso")
            else:
                user = Providers.objects.get(username=username)
                store_items = Store.objects.filter(provider=user)
                for item in store_items:
                    if OrderDetails.objects.filter(store=item, status="S"):
                        return homepage_provider(request, "Impossibile cancellare il tuo account, un tuo prodotto è presente in un ordine in sospeso, completa gli ordini prima di cancellare il tuo account")
                    delete_product_from_store(request, item.id)
            if check_password(psw, user.password):
                settings.GLOBAL_VARIABLE = ""
                user.delete()
                return render(request, 'account_pages/index.html', {'message': 'Account eliminato con successo'})
            else:
                return homepage_client(request, 'Password Errata')
        except Users.DoesNotExist:
            return JsonResponse({"successo": False, "messaggio": "Utente non trovato"})

    return JsonResponse({"successo": False, "messaggio": "Metodo non supportato"})


def search_product(request):
    if request.method == 'POST':
        providers = Providers.objects.all()
        options_data_cat = []
        options_data_prov = []
        context = {}
        desc_prod_insert = request.POST.get('search', '')
        if desc_prod_insert == "":
            context['show_options'] = True
            return homepage_client(request, context)

        similar_store = Store.objects.filter(desc_prod__icontains=desc_prod_insert)
        if similar_store.count() == 0:
            context['show_options'] = True
            return homepage_client(request, "Non ci sono prodotti con descrizione simile a quella cercata")
        context['show_options'] = False  # Se il messaggio è "Password Corretta", mostra il form di aggiornamento
        context['show_text'] = False
        # Costruisci una lista dei dati del negozio
        store_data = []
        for store in similar_store:
            provider_username = store.provider.username
            subcategory_name = store.subcategory.name
            price = store.price_product
            description = store.desc_prod
            discount = "" if store.discount is None else f"{store.discount}%"
            av_quant = store.available_quantity
            id_store = store.id
            store_data.append({
                'fornitore_username': provider_username,
                'sottocategoria_nome': subcategory_name,
                'prezzo': price,
                'descrizione': description,
                'sconto': discount,
                'quantita_disponibile': f"{av_quant} {store.measure_units.abbreviation}",
                'id_store': id_store,
            })

        options_data_cat.append({
            'store_data': store_data
        })

        for provider in providers:
            options_data_prov.append({
                'id_provider': provider.id,
                'name_provider': provider.username,
            })

        context = {
            'options_data_cat': options_data_cat,
            'options_data_prov': options_data_prov,
        }

        return render(request, 'client/homepage_client.html', context)

    return render(request, 'client/homepage_client.html')


def filter_orders_by_status(request):
    if request.method == 'GET':
        status = request.GET.get('status', '')
        orders_data = []
        username = settings.GLOBAL_VARIABLE

        user = get_object_or_404(Users, username=username)

        order_items = Orders.objects.filter(user=user, status=status).order_by('-date_order')

        for item in order_items:
            timestamp = float(item.date_order)
            date_time = datetime.fromtimestamp(timestamp)
            date_only = date_time.strftime('%d.%m.%Y %H:%M')
            if item.status=="S" :
                txt_status = "In sospeso"
            elif item.status=="C" :
                txt_status = "Completato"
            order_info = {
                'status_order': txt_status,
                'order_id': item.id,
                'date_order': date_only,
            }
            orders_data.append(order_info)

        return JsonResponse(orders_data, safe=False)

    return render(request, 'client/homepage_client.html')


def get_store_data_for_prov(category_name):
    store_data = []
    username_provider = settings.GLOBAL_VARIABLE
    provider = Providers.objects.get(username=username_provider)

    try:
        category = Categories.objects.get(name=category_name)
    except Categories.DoesNotExist:
        # Gestisci il caso in cui la categoria non esista
        return store_data

    subcategories = Subcategories.objects.filter(category=category)
    for subcategory in subcategories:
        stores = Store.objects.filter(subcategory=subcategory, provider=provider)

        for store in stores:
            measure_unit = store.measure_units.abbreviation
            subcategory_name = subcategory.name  # Accedi direttamente al nome della sottocategoria
            price = store.price_product
            description = store.desc_prod
            if store.discount is None:
                discount = ""
            else:
                discount = f"{store.discount}%"
            av_quant = store.available_quantity
            id_store = store.id
            store_data.append({
                'sottocategoria_nome': subcategory_name,
                'prezzo': price,
                'descrizione': description,
                'sconto': discount,
                'quantita_disponibile': f"{av_quant} {measure_unit}",
                'id_store': id_store,
            })

    return store_data


def get_store_data_for_single_cat_for_prov(request):
    if request.method == 'GET':
        category_name = request.GET.get('category', '')

        username_provider = settings.GLOBAL_VARIABLE
        provider = Providers.objects.get(username=username_provider)
        store_data = []

        try:
            category = Categories.objects.get(name=category_name)
        except Categories.DoesNotExist:
            # Gestisci il caso in cui la categoria non esista
            return JsonResponse(store_data, safe=False)

        subcategories = Subcategories.objects.filter(category=category)
        for subcategory in subcategories:
            stores = Store.objects.filter(subcategory=subcategory, provider=provider)

            for store in stores:
                measure_unit = store.measure_units.abbreviation
                subcategory_name = subcategory.name  # Accedi direttamente al nome della sottocategoria
                price = store.price_product
                description = store.desc_prod
                if store.discount is None:
                    discount = ""
                else:
                    discount = f"{store.discount}%"
                av_quant = store.available_quantity
                id_store = store.id
                store_data.append({
                    'sottocategoria_nome': subcategory_name,
                    'prezzo': price,
                    'descrizione': description,
                    'sconto': discount,
                    'quantita_disponibile': f"{av_quant} {measure_unit}",
                    'id_store': id_store,
                })

        return JsonResponse(store_data, safe=False)


def get_store_data_for_single_subcat_for_prov(request):
    if request.method == 'GET':
        subcategory_id = request.GET.get('subcategory_id', '')
        username_provider = settings.GLOBAL_VARIABLE
        provider = Providers.objects.get(username=username_provider)
        # Inizializza una query di filtro per il modello Store
        filter_query = Q()

        # Aggiungi la clausola di filtro per la sottocategoria, se specificata
        if subcategory_id:
            filter_query &= Q(subcategory_id=subcategory_id, provider=provider)

        # Esegue la query per ottenere i negozi filtrati
        stores = Store.objects.filter(filter_query)

        store_data = []

        for store in stores:
            measure_unit = store.measure_units.abbreviation
            subcategory_name = store.subcategory.name
            price = store.price_product
            description = store.desc_prod
            av_quant = store.available_quantity
            discount = f"{store.discount}%" if store.discount else ""  # Gestisci il caso in cui lo sconto sia None
            id_store = store.id

            # Aggiungi i dettagli del negozio alla lista dei dati del negozio
            store_data.append({
                'sottocategoria_nome': subcategory_name,
                'prezzo': price,
                'descrizione': description,
                'sconto': discount,
                'quantita_disponibile': f"{av_quant} {measure_unit}",
                'id_store': id_store,
            })

    return JsonResponse(store_data, safe=False)


def search_product_for_prov(request):
    if request.method == 'POST':
        options_data_cat = []
        username_provider = settings.GLOBAL_VARIABLE
        provider = Providers.objects.get(username=username_provider)
        context = {}
        desc_prod_insert = request.POST.get('search', '')
        if desc_prod_insert == "":
            context['show_options'] = True
            return homepage_provider(request, context)

        similar_store = Store.objects.filter(desc_prod__icontains=desc_prod_insert, provider=provider)
        if similar_store.count() == 0:
            context['show_options'] = True
            return homepage_provider(request, "Non ci sono prodotti con descrizione simile a quella cercata")
        context['show_options'] = False  # Se il messaggio è "Password Corretta", mostra il form di aggiornamento
        context['show_text'] = False
        # Costruisci una lista dei dati del negozio
        store_data = []
        for store in similar_store:
            subcategory_name = store.subcategory.name
            price = store.price_product
            description = store.desc_prod
            discount = "" if store.discount is None else f"{store.discount}%"
            av_quant = store.available_quantity
            id_store = store.id
            store_data.append({
                'sottocategoria_nome': subcategory_name,
                'prezzo': price,
                'descrizione': description,
                'sconto': discount,
                'quantita_disponibile': f"{av_quant} {store.measure_units.abbreviation}",
                'id_store': id_store,
            })

        options_data_cat.append({
            'store_data': store_data
        })

        context = {
            'options_data_cat': options_data_cat,
        }

        return render(request, 'provider/homepage_provider.html', context)

    return render(request, 'provider/homepage_provider.html')


def delete_product_from_store(request, store_id):
    store = Store.objects.get(pk=store_id)
    order_details = OrderDetails.objects.filter(store=store)
    cart = Cart.objects.filter(store=store)

    cart.delete()
    order_details.delete()
    store.delete()

    return homepage_provider(request, 'Prodotto eliminato con successo')


def get_data_product(store_id):
    store_data = []

    store_items = Store.objects.filter(pk=store_id)

    for item in store_items:
        if item.discount is None:
            sconto = 0
        else:
            sconto = item.discount
        store_info = {
            'quantita_disponibile': item.available_quantity,
            'prezzo': item.price_product,
            'descrizione': item.desc_prod,
            'unita_misura': item.measure_units.name,
            'sconto': sconto,
            'id_store': item.id,
        }
        store_data.append(store_info)

    return store_data


def update_datas_product(request):
    if request.method == 'POST':
        id_store = request.POST.get('store_id', '')
        available_quantity = request.POST.get('quantity', '')
        price_product = request.POST.get('price', '')
        desc_product = request.POST.get('desc', '')
        discount = request.POST.get('discount', '')

        # Ottieni l'utente attuale per escluderlo dalla query
        product = Store.objects.get(pk=id_store)

        product.available_quantity = available_quantity
        product.price_product = price_product
        product.desc_prod = desc_product
        if discount != "0":
            product.discount = discount
        product.save()
        return homepage_provider(request, "Dati modificati con successo")


def insert_product_page(request):
    if settings.GLOBAL_VARIABLE == "":
        return render(request, 'account_pages/index.html', {'message': 'Devi accedere per arrivare a questa pagina'})
    categories = Categories.objects.all()
    options_data_cat = []

    for category in categories:
        options_data_cat.append({
            'id': category.id,
            'name': category.name,
        })

    measure_units = Measure_units.objects.all()
    options_data_meausure = []

    for measure_unit in measure_units:
        options_data_meausure.append({
            'id': measure_unit.id,
            'name': measure_unit.name,
        })

    context = {
        'options_data_cat': options_data_cat,
        'options_data_meausure': options_data_meausure,
        'show_options': True,
    }
    return render(request, 'provider/insert_product_page.html', context)


def insert_product(request):
    username_provider = settings.GLOBAL_VARIABLE
    provider = Providers.objects.get(username=username_provider)
    subcategory_id = request.POST.get('subcategories', '')
    subcategories = Subcategories.objects.get(pk=subcategory_id)
    measure_unit_id = request.POST.get('unita_misura', '')
    measure_units = Measure_units.objects.get(pk=measure_unit_id)
    available_quantity = request.POST.get('quantity', '')
    price_product = request.POST.get('price', '')
    desc_product = request.POST.get('desc', '')
    discount = request.POST.get('discount', '')
    if discount=="":
        discount = None

    Store.objects.create(provider=provider, subcategory=subcategories, measure_units=measure_units, available_quantity=available_quantity, price_product=price_product, desc_prod=desc_product, discount=discount)

    return homepage_provider(request, 'Prodotto inserito nel magazzino')


def orders_history_provider(request, message=None):
    if not settings.GLOBAL_VARIABLE:
        return render(request, 'account_pages/index.html', {'message': 'Devi accedere per arrivare a questa pagina'})

    orders_data = get_orders_data_provider(settings.GLOBAL_VARIABLE)

    context = {
        'orders_data': orders_data  # Assicurati che qui stai passando i dati del carrello senza incorrere in sovrascritture accidentali
    }
    if message:
        context['message'] = message
    return render(request, 'provider/orders_page_provider.html', context)


def get_orders_data_provider(username):
    orders_data = []

    if not username:
        return JsonResponse({'error': 'Username is required'}, status=400)

    provider = get_object_or_404(Providers, username=username)

    # Ottieni gli ordini unici associati al fornitore
    orders = Orders.objects.filter(orderdetails__store__provider=provider).distinct()

    for order in orders:
        txt_status = "Completato"

        # Controlla lo stato di tutti gli order_details relativi all'ordine specifico del provider
        order_details_statuses = set(OrderDetails.objects.filter(order=order, store__provider=provider).values_list('status', flat=True))
        if 'S' in order_details_statuses:  # Se anche uno ha stato "S" (in sospeso)
            txt_status = "In sospeso"

        timestamp = float(order.date_order)
        date_time = datetime.fromtimestamp(timestamp)
        date_only = date_time.strftime('%d.%m.%Y %H:%M')
        order_info = {
            'status_order': txt_status,
            'customer': order.user.username,
            'order_id': order.id,
            'data_order': date_only,
        }
        orders_data.append(order_info)

    return orders_data



def order_details_provider(request, order_id):
    if not settings.GLOBAL_VARIABLE:
        return render(request, 'account_pages/index.html', {'message': 'Devi accedere per arrivare a questa pagina'})

    orders_details_data = get_order_details_data_for_provider(order_id)

    context = {
        'orders_details_data': orders_details_data  # Assicurati che qui stai passando i dati del carrello senza incorrere in sovrascritture accidentali
    }

    return render(request, 'provider/orders_details_page_provider.html', context)


def get_order_details_data_for_provider(order_id):
    username_provider = settings.GLOBAL_VARIABLE
    order_details_data = []
    provider = get_object_or_404(Providers, username=username_provider)
    store_provider = Store.objects.filter(provider=provider)
    order = get_object_or_404(Orders, pk=order_id)

    for s in store_provider:
        order_details_items = OrderDetails.objects.filter(order=order, store=s)

        for item in order_details_items:

            store = item.store
            price_product = Decimal(str(store.price_product))
            price = price_product * item.quantity
            if item.status=="S" :
                txt_status = "In sospeso"
            elif item.status=="A" :
                txt_status = "Accettato"
            else:
                txt_status = "Rifiutato"
            if store.discount is None:
                price_discounted = 0
                discount = ""
            else:
                price_discounted = (price_product * (1 - Decimal(store.discount) / 100)) * item.quantity
                discount = f"{store.discount}%"
            order_details_info = {
                'order_details_id': item.id,
                'status_order': order.status,
                'order_id': order.id,
                'quantita': f"{item.quantity} {store.measure_units.abbreviation}",
                "prezzo_totale": f"{price:.2f}",
                'prezzo_totale_scontato': f"{price_discounted:.2f}",
                'descrizione': store.desc_prod,
                'sconto': discount,
                'status': txt_status,
            }
            order_details_data.append(order_details_info)

    return order_details_data


def accept_deny_product(request, order_detail_id, control):
    order_detail = get_object_or_404(OrderDetails, pk=order_detail_id)
    order = order_detail.order

    if control == 1:
        order_detail.status = "A"
        order_detail.save()
        message = 'Prodotto accettato con successo'
    else:
        order_detail.status = "R"
        order_detail.save()
        message = 'Prodotto rifiutato con successo'

    # Controllo se tutti gli order_details dell'ordine sono accettati o rifiutati
    order_status = "C"  # Assume che l'ordine sia completato
    for item in order.orderdetails_set.all():
        if item.status == "S":  # Se almeno uno è in sospeso
            order_status = "S"  # Imposta lo stato dell'ordine a "in sospeso"
            break

    # Aggiorna lo stato dell'ordine se necessario
    if order_status != order.status:
        order.status = order_status
        order.save()

    return orders_history_provider(request, message)


def accept_deny_order(request, control):
    order_id = request.POST.get('order_id', '')
    order = get_object_or_404(Orders, pk=order_id)

    order_details = OrderDetails.objects.filter(order=order, store__provider__username=settings.GLOBAL_VARIABLE)

    for order_detail in order_details:
        if order_detail.status == "S" and control == 1:
            order_detail.status = "A"
            order_detail.save()
        elif order_detail.status == "S" and control == 2:
            order_detail.status = "R"
            order_detail.save()

    order_status = "C"  # Assume che l'ordine sia completato
    for item in order.orderdetails_set.all():
        if item.status == "S":  # Se almeno uno è in sospeso
            order_status = "S"  # Imposta lo stato dell'ordine a "in sospeso"
            break

    # Aggiorna lo stato dell'ordine se necessario
    if order_status != order.status:
        order.status = order_status
        order.save()

    if control == 1:
        return orders_history_provider(request, "Ordine accettato con successo")
    else:
        return orders_history_provider(request, "Ordine rifiutato con successo")



















