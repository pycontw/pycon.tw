import './polyfills'

import {Application} from 'stimulus'
import {MenuController} from './controllers/menu'
import {TopNavController} from './controllers/nav'

const application = Application.start()
application.register('topNav', TopNavController)
application.register('menu', MenuController)
