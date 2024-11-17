import { DateTime } from 'luxon'

const commonUtil = () => {

    const isUrlAllowed = (url: string, whiteList: string[]): boolean => {
        return whiteList.some(pattern => matchUrl(url, pattern));
    };

    const matchUrl = (url: string, pattern: string): boolean => {
        // 정규 표현식 패턴을 만듭니다.
        const regexPattern = new RegExp(`^${pattern.replace(/\*\*/g, '.*').replace(/\*/g, '[^/]*')}$`);

        // 주어진 URL이 패턴과 일치하는지 여부를 반환합니다.
        return regexPattern.test(url);
    }

    const scrollToBottom = (selector:string, top: number = 0, behavior: string = 'smooth') => {
        const targetSelector = document.querySelector(selector);

        // 엘리먼트가 존재하고, 스크롤이 가능한 경우에만 맨 아래로 스크롤
        if (targetSelector && targetSelector.scrollHeight > targetSelector.clientHeight) {
            targetSelector.scrollTop = targetSelector.scrollHeight
        }
    }

    const formatDate = (format: string = 'yyyy.MM.dd HH:mm:ss', pocket?: DateTime): string => {
        const dateToFormat = pocket || DateTime.now();

        return dateToFormat.toFormat(format);
    }

    const isNotEmpty = (value: string): boolean => {
        return value.trim() !== '';
    }

    return {
        isUrlAllowed,
        matchUrl,
        scrollToBottom,
        formatDate,
        isNotEmpty
    }
};
export default commonUtil;
