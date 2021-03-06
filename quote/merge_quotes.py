# coding: utf-8

from datetime import date
from sqlalchemy import and_
from models import Quote, Session
from indicator.basic import change_percent


def group_quotes_by_week(quotes):
    first = quotes[0]
    start_week_date = first.datetime
    year = start_week_date.year
    week = start_week_date.isocalendar()[1]
    day_quotes_of_week = [first]
    week_quote_groups = []
    for quote in quotes[1:]:
        quote_date = quote.datetime
        if quote_date.year == year and quote_date.isocalendar()[1] == week:
            day_quotes_of_week.append(quote)
        else:
            week_quote_groups.append(day_quotes_of_week)
            day_quotes_of_week = [quote]
            year = quote.datetime.year
            week = quote.datetime.isocalendar()[1]
    week_quote_groups.append(day_quotes_of_week)

    return week_quote_groups


def merge_quotes(quotes):
    first = quotes[0]
    last = quotes[-1]

    pre_close = first.pre_close
    open = first.open
    high = max(q.high for q in quotes)
    low = min(q.low for q in quotes)
    close = last.close
    volume = sum(q.volume for q in quotes)
    amount = sum(q.amount for q in quotes)
    change = last.close - first.pre_close
    percent = change_percent(close, pre_close)

    merged = Quote(
        code=first.code,
        datetime=first.datetime,
        period='TBD',
        open=open,
        close=close,
        low=low,
        high=high,
        pre_close=pre_close,
        change=change,
        percent=percent,
        volume=volume,
        amount=amount
    )

    if last.turnover:
        estimate_shares = int(last.volume / last.turnover * 100)
        merged.turnover = round(float(volume) / estimate_shares * 100, 3)

    return merged


def create_week_quote(day_quotes):
    week_quotes = []
    week_groups = group_quotes_by_week(day_quotes)
    for wg in week_groups:
        quote = merge_quotes(wg)
        quote.period = 'w1'
        week_quotes.append(quote)

    return week_quotes


if __name__ == '__main__':
    start = date(2016, 6, 6)
    end = date(2016, 6, 8)

    ss = Session()

    securities = ss.query(Quote.code).distinct().all()

    for sec in securities:
        day_quotes = ss.query(Quote).filter(
            and_(
                Quote.code == sec.code,
                Quote.period == 'd1',
                Quote.datetime >= start,
                Quote.datetime <= end
            )
        ).order_by(Quote.datetime.asc()).all()

        if not day_quotes:
            continue

        week_quotes = create_week_quote(day_quotes)

        ss.add_all(week_quotes)
        ss.commit()
