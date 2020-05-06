import React from 'react';
import css from './ResultView.module.css'

export default ({result}) => (
    <li className="sui-result">
        <ul className={css.url}>
            <span className="sui-result__value" dangerouslySetInnerHTML={{__html: result.url.raw}}/>
        </ul>
        <div className="sui-result__header">

            <a href={result.title.raw}
               className={css.header}
               dangerouslySetInnerHTML={{__html: result.title.raw}}
            />
        </div>

        <ul className="sui-result__details">
            <li className={css.details}>
                <span className="sui-result__value" dangerouslySetInnerHTML={{__html: result.body.snippet}}/>
            </li>
            <li>
                <span className="sui-result__key">Found on Date</span>
                <span className="sui-result__value" dangerouslySetInnerHTML={{__html: result.date.raw}}/>
            </li>

        </ul>
    </li>

)