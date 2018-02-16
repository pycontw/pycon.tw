import {Application} from 'stimulus'
import {TopNavController} from './controllers/nav'

const application = Application.start()
application.register('topNav', TopNavController)
