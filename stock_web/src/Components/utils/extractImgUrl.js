export const extractImgUrl = (path) => {
    let imgURL
    try {
        imgURL = require(`../../forecast_image/${path}`)
    } catch (err) {
        if (err.code !== "MODULE_NOT_FOUND") {
            throw err
        }
        imgURL = ""
    }
    return imgURL
}