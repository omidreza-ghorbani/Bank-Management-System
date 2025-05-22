# پیام‌های عمومی
WELCOME_MESSAGE = "به سیستم بانکداری مدرن خوش آمدید"
LOGIN_TITLE = "ورود به سیستم"
REGISTER_TITLE = "ثبت نام"
ERROR_TITLE = "خطا"
SUCCESS_TITLE = "موفقیت"

# پیام‌های خطا
INVALID_PASSWORD = "رمز عبور باید حداقل 8 کاراکتر و شامل حروف و اعداد باشد"
LOGIN_ERROR = "شناسه کاربری یا رمز عبور اشتباه است"
ACCOUNT_NOT_FOUND = "حساب مورد نظر یافت نشد"
UNAUTHORIZED_ACCESS = "دسترسی غیرمجاز"
INSUFFICIENT_BALANCE = "موجودی کافی نیست"
INVALID_AMOUNT = "مبلغ باید مثبت باشد"
LOGIN_REQUIRED = "لطفا ابتدا وارد شوید"

# پیام‌های موفقیت
REGISTER_SUCCESS = "ثبت نام با موفقیت انجام شد. شناسه مشتری شما: {}"
ACCOUNT_CREATED = "حساب با موفقیت ایجاد شد. شماره حساب: {}"
DEPOSIT_SUCCESS = "واریز با موفقیت انجام شد. موجودی جدید: {}"
WITHDRAW_SUCCESS = "برداشت با موفقیت انجام شد. موجودی جدید: {}"
TRANSFER_SUCCESS = "انتقال با موفقیت انجام شد. مبلغ {} منتقل شد"

# برچسب‌های فرم
CUSTOMER_ID_LABEL = "شناسه مشتری:"
PASSWORD_LABEL = "رمز عبور:"
NAME_LABEL = "نام:"
ACCOUNT_LABEL = "حساب:"
AMOUNT_LABEL = "مبلغ:"
FROM_ACCOUNT_LABEL = "حساب مبدا:"
TO_ACCOUNT_LABEL = "حساب مقصد:"

# دکمه‌ها
LOGIN_BUTTON = "ورود"
REGISTER_BUTTON = "ثبت نام"
BACK_BUTTON = "بازگشت"
LOGOUT_BUTTON = "خروج"
CREATE_ACCOUNT_BUTTON = "ایجاد حساب جدید"
DEPOSIT_BUTTON = "واریز"
WITHDRAW_BUTTON = "برداشت"
TRANSFER_BUTTON = "انتقال"
SELECT_ACCOUNT_LABEL = "انتخاب حساب:"
SHOW_HISTORY_BUTTON = "نمایش تاریخچه"
TRANSACTION_HISTORY_BUTTON = "مشاهده تاریخچه تراکنش‌ها"

# عنوان‌های پنجره‌ها
APP_TITLE = "سیستم بانکداری مدرن"
TRANSFER_TITLE = "انتقال وجه"
TRANSACTION_HISTORY_TITLE = "تاریخچه تراکنش‌ها:"

# فرمت‌های نمایش
BALANCE_FORMAT = "موجودی حساب: {}"
ACCOUNT_INFO_FORMAT = "حساب: {}"
BALANCE_INFO_FORMAT = "موجودی: {:.2f} ریال"
WELCOME_USER_FORMAT = "Welcome {}!"

# انواع تراکنش‌ها
TRANSACTION_TYPES = {
    'DEPOSIT': 'واریز',
    'WITHDRAW': 'برداشت',
    'TRANSFER_OUT': 'انتقال خروج',
    'TRANSFER_IN': 'انتقال ورود'
}

# تنظیمات برنامه
MIN_PASSWORD_LENGTH = 8
PRIORITY_TRANSFER_AMOUNT = 1000000  # مبلغ تراکنش‌های با اولویت بالا

# پیام‌های تراکنش
TRANSACTION_FORMAT = "{} - {}: {} - {}"

# توضیحات تراکنش‌ها
CASH_DEPOSIT = "واریز نقدی"
CASH_WITHDRAWAL = "برداشت نقدی"
TRANSFER_TO_FORMAT = "انتقال به {}"
TRANSFER_FROM_FORMAT = "انتقال از {}"

# فرمت‌های شناسه
CUSTOMER_ID_FORMAT = "CUST{:04d}"
ACCOUNT_NUMBER_FORMAT = "ACC{:06d}"

# مسیر فایل داده
DATA_FILE_PATH = 'data/bank_data.json'

# کلیدهای داده
DATA_CUSTOMERS_KEY = 'customers'
DATA_ACCOUNTS_KEY = 'accounts'
DATA_CUSTOMER_ID_KEY = 'customer_id'
DATA_NAME_KEY = 'name'
DATA_PASSWORD_HASH_KEY = 'password_hash'
DATA_ACCOUNT_NUMBER_KEY = 'account_number'
DATA_BALANCE_KEY = 'balance'
DATA_TRANSACTION_HISTORY_KEY = 'transaction_history' 