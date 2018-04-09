import './polyfills'

import {Application} from 'stimulus'
import {MediaPopupController} from './controllers/popup'
import {MenuController} from './controllers/menu'
import {TopNavController} from './controllers/nav'

const application = Application.start()
application.register('mediaPopup', MediaPopupController)
application.register('menu', MenuController)
application.register('topNav', TopNavController)
