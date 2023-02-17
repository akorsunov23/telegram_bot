from telebot.handler_backends import State, StatesGroup


class StateLowprice(StatesGroup):
	name = State()
	city = State()
	region_selection = State()
	amount_hostels = State()
	start_date = State()
	end_date = State()
	foto = State()
	amount_foto = State()


class StateHighprice(StatesGroup):
	name = State()
	city = State()
	region_selection = State()
	amount_hostels = State()
	start_date = State()
	end_date = State()
	foto = State()
	amount_foto = State()


class StateBestdeal(StatesGroup):
	name = State()
	city = State()
	region_selection = State()
	start_price = State()
	end_price = State()
	amount_hostels = State()
	start_date = State()
	end_date = State()
	start_distance = State()
	end_distance = State()
	foto = State()
	amount_foto = State()


class StateHistory(StatesGroup):
	amount_requests = State()
